#nullable enable
using System;
using System.Collections.Generic;
using System.Linq;
using R3;
using Workflow.Examples.Application;
using Workflow.Examples.Presentation;

internal static class ViewModelChecks
{
    private static int _count;

    private static void Check(bool value, string name)
    {
        if (!value)
        {
            throw new Exception(name);
        }
        _count++;
        Console.WriteLine("PASS " + name);
    }

    private static void Main()
    {
        using var inventory = new FakeInventory();
        var vm = new InventorySlotViewModel(inventory);
        var seen = new List<InventorySlotState>();
        using var binding = vm.State.Subscribe(seen.Add);
        Check(seen.Count == 1 && seen[0].Title == "Potion" && seen[0].QuantityText == "3" && seen[0].CanActivate,
            "initial coherent replay without constructing Unity UI");
        inventory.Source.Value = new InventoryState("potion", "Potion", 3);
        Check(seen.Count == 1, "equal display values deduplicated");
        vm.Activate();
        Check(inventory.LastId == "potion" && inventory.Commands == 1, "command uses current item identity");
        inventory.Source.Value = new InventoryState("key", "Potion", 3);
        Check(seen.Count == 1, "identity change does not force unchanged rendering");
        vm.Activate();
        Check(inventory.LastId == "key", "identity changes still update command target");
        inventory.Source.Value = new InventoryState("key", "Key", 0);
        Check(seen.Count == 2 && seen[1].Title == "Key" && seen[1].QuantityText == "0" && !seen[1].CanActivate,
            "disabled projection is coherent");
        int commands = inventory.Commands;
        vm.Activate();
        Check(inventory.Commands == commands, "disabled command is gated");
        inventory.Source.Value = new InventoryState("", "Empty", 4);
        Check(!seen.Last().CanActivate, "missing identity disables action");
        int beforeDispose = seen.Count;
        vm.Dispose();
        vm.Dispose();
        inventory.Source.Value = new InventoryState("late", "Late", 8);
        Check(seen.Count == beforeDispose, "disposed VM rejects late projection");
        vm.Activate();
        Check(inventory.Commands == commands, "disposed VM cannot issue commands");
        using var second = new InventorySlotViewModel(inventory);
        second.Activate();
        Check(inventory.LastId == "late", "VM disposal does not dispose borrowed application service");
        var failingInventory = new ThrowingInventory();
        var failingVm = new InventorySlotViewModel(failingInventory);
        bool completed = false;
        using var failingBinding = failingVm.State.Subscribe(_ => { }, (Result _) => completed = true);
        Exception? disposalError = null;
        try
        {
            failingVm.Dispose();
        }
        catch (Exception error)
        {
            disposalError = error;
        }
        Check(ReferenceEquals(disposalError, failingInventory.Failure), "subscription disposal failure is preserved");
        Check(completed, "VM state completes even if subscription disposal fails");
        failingVm.Activate();
        failingVm.Dispose();
        Check(failingInventory.Commands == 0, "failed teardown remains closed and repeat disposal is harmless");
        foreach (var assembly in new[] { typeof(InventorySlotViewModel).Assembly, typeof(IInventory).Assembly,
            typeof(Workflow.Examples.ScopedContext<string>).Assembly })
        {
            Check(!assembly.GetReferencedAssemblies().Any(x => x.Name!.StartsWith("Unity", StringComparison.Ordinal) ||
                x.Name.StartsWith("VContainer", StringComparison.Ordinal) ||
                x.Name == "ApiCheck" || x.Name == "UiCheck"),
                assembly.GetName().Name + " compiled references are engine/container independent");
        }
        Check(!typeof(Workflow.Examples.ScopedContext<string>).Assembly.GetReferencedAssemblies().Any(x => x.Name == "R3"),
            "Core reference assembly has no R3 dependency");
        Console.WriteLine($"{_count} ViewModel/boundary checks passed.");
    }

    private sealed class ThrowingInventory : IInventory
    {
        public Exception Failure { get; } = new InvalidOperationException("subscription release fault");
        public Observable<InventoryState> State { get; }
        public int Commands { get; private set; }

        public ThrowingInventory()
        {
            State = Observable.Create<InventoryState>(observer =>
            {
                observer.OnNext(new InventoryState("potion", "Potion", 1));
                return Disposable.Create(() => throw Failure);
            });
        }

        public void Activate(string itemId)
        {
            Commands++;
        }
    }

    private sealed class FakeInventory : IInventory, IDisposable
    {
        public ReactiveProperty<InventoryState> Source
        {
            get;
        } =
            new ReactiveProperty<InventoryState>(new InventoryState("potion", "Potion", 3));
        public Observable<InventoryState> State => Source;
        public int Commands
        {
            get; private set;
        }
        public string LastId { get; private set; } = string.Empty;

        public void Activate(string itemId)
        {
            LastId = itemId;
            Commands++;
        }

        public void Dispose()
        {
            Source.Dispose();
        }
    }
}
