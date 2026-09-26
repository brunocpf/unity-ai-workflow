#nullable enable
using System;
using System.Threading;
using Workflow.Examples;

internal static class PureChecks
{
    private static int _count;

    private static void Check(bool condition, string name)
    {
        if (!condition)
        {
            throw new Exception(name);
        }
        _count++;
        Console.WriteLine("PASS " + name);
    }

    private static void Main()
    {
        var context = new ScopedContext<string>();
        Check(context.Current == null, "initially empty");
        using (var outer = context.Enter("outer"))
        {
            using (var inner = context.Enter("inner"))
            {
                Check(context.Current == "inner", "nested lookup");
            }
            Check(context.Current == "outer", "restore parent");
        }
        Check(context.Current == null, "restore empty");
        try
        {
            using var scope = context.Enter("throw");
            throw new Exception("expected");
        }
        catch (Exception) { }
        Check(context.Current == null, "exception restores");
        var a = context.Enter("a");
        var b = context.Enter("b");
        bool threw = false;
        try
        {
            a.Dispose();
        }
        catch (InvalidOperationException)
        {
            threw = true;
        }
        Check(threw && context.Current == "b", "reject out-of-order without corruption");
        b.Dispose();
        a.Dispose();
        threw = false;
        try
        {
            a.Dispose();
        }
        catch (InvalidOperationException)
        {
            threw = true;
        }
        Check(threw, "reject double dispose");
        var original = context.Enter("copy");
        var copy = original;
        original.Dispose();
        threw = false;
        try
        {
            copy.Dispose();
        }
        catch (InvalidOperationException)
        {
            threw = true;
        }
        Check(threw, "reject copied scope");
        var oldGeneration = context.Generation;
        var stale = context.Enter("stale");
        context.Reset();
        using (var fresh = context.Enter("fresh"))
        {
            stale.Dispose();
            Check(context.Current == "fresh" && !ReferenceEquals(oldGeneration, context.Generation),
                "stale scope cannot restore prior session");
        }
        Exception? workerError = null;
        var thread = new Thread(() =>
        {
            try
            {
                _ = context.Current;
            }
            catch (Exception e)
            {
                workerError = e;
            }
        });
        thread.Start();
        thread.Join();
        Check(workerError is InvalidOperationException, "reject worker access");
        for (int i = 0; i < 1000; i++)
        {
            using var warm = context.Enter("warm");
        }
        long before = GC.GetAllocatedBytesForCurrentThread();
        for (int i = 0; i < 100000; i++)
        {
            using var warm = context.Enter("warm");
        }
        long allocated = GC.GetAllocatedBytesForCurrentThread() - before;
        Check(allocated == 0, "100000 warm scope entries: zero managed allocation on this runtime");
        var latest = new LatestRequest();
        var first = latest.Begin();
        var second = latest.Begin();
        Check(!first.IsCurrent && second.IsCurrent, "latest request wins");
        latest.Dispose();
        Check(!second.IsCurrent, "disposed owner invalidates request");
        threw = false;
        try
        {
            latest.Begin();
        }
        catch (ObjectDisposedException)
        {
            threw = true;
        }
        Check(threw, "disposed request owner rejects new work");
        Check(!default(LatestRequest.Ticket).IsCurrent, "default ticket invalid");
        Console.WriteLine($"{_count} checks passed.");
    }
}
