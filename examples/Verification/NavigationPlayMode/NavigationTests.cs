#nullable enable
using System;
using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.LowLevel;
using UnityEngine.TestTools;
using UnityEngine.UIElements;
using Workflow.Examples.UI.Navigation;

public sealed class NavigationTests
{
    private GameObject _object = null!;
    private VisualElement _host = null!;
    private UiNavigationStack _stack = null!;
    private Keyboard _keyboard = null!;
    private Gamepad _gamepad = null!;
    private Mouse _mouse = null!;
    private bool _blocked;
    private int _activations;
    private int _disposals;
    private InputSettings.BackgroundBehavior _background;
    private InputSettings.EditorInputBehaviorInPlayMode _editorInput;

    [UnitySetUp]
    public IEnumerator SetUp()
    {
        _background = InputSystem.settings.backgroundBehavior;
        _editorInput = InputSystem.settings.editorInputBehaviorInPlayMode;
        InputSystem.settings.backgroundBehavior = InputSettings.BackgroundBehavior.IgnoreFocus;
        InputSystem.settings.editorInputBehaviorInPlayMode =
            InputSettings.EditorInputBehaviorInPlayMode.AllDeviceInputAlwaysGoesToGameView;
        _keyboard = InputSystem.AddDevice<Keyboard>();
        _gamepad = InputSystem.AddDevice<Gamepad>();
        _mouse = InputSystem.AddDevice<Mouse>();
        _object = new GameObject("Navigation fixture");
        var renderer = _object.AddComponent<PanelRenderer>();
        renderer.RegisterUIReloadCallback((_, root, version) => _host = root.Q("navigation-host"));
        renderer.panelSettings = Resources.Load<PanelSettings>("NavigationPanel");
        renderer.visualTreeAsset = Resources.Load<VisualTreeAsset>("NavigationHost");
        yield return Frames();
        if (_host == null || _host.panel == null)
        {
            throw new AssertionException("Real runtime panel required");
        }
        _stack = new UiNavigationStack(_host, blocked => _blocked = blocked,
            () => _stack.PushScreen(Menu()));
        _activations = 0;
        _disposals = 0;
    }

    [UnityTearDown]
    public IEnumerator TearDown()
    {
        _stack?.Dispose();
        UnityEngine.Object.Destroy(_object);
        InputSystem.RemoveDevice(_keyboard);
        InputSystem.RemoveDevice(_gamepad);
        InputSystem.RemoveDevice(_mouse);
        InputSystem.settings.backgroundBehavior = _background;
        InputSystem.settings.editorInputBehaviorInPlayMode = _editorInput;
        yield return null;
    }

    [UnityTest]
    public IEnumerator KeyboardAndControllerUseNativeMoveSubmitAndCancel()
    {
        yield return KeyPress(Key.Escape);
        Assert.That(_stack.Count, Is.EqualTo(1));
        AssertFocused("first");
        yield return KeyPress(Key.DownArrow);
        AssertFocused("second"); // Disabled middle button must be skipped.
        yield return KeyPress(Key.Enter);
        Assert.That(_activations, Is.EqualTo(1));
        yield return PadPress(GamepadButton.DpadDown);
        AssertFocused("third");
        yield return PadPress(GamepadButton.South);
        Assert.That(_activations, Is.EqualTo(2));
        yield return PadPress(GamepadButton.East);
        Assert.That(_stack.Count, Is.Zero);
        Assert.That(_blocked, Is.False);
        Assert.That(_disposals, Is.EqualTo(1));
    }

    [UnityTest]
    public IEnumerator ModalRestoresFocusAndPendingHandoffsCannotStealIt()
    {
        _stack.PushScreen(Menu());
        yield return Frames();
        yield return KeyPress(Key.DownArrow);
        UiStackEntry screen = _stack.Top!;
        _stack.PushModal(Menu());
        yield return Frames();
        Assert.That(screen.View.enabledInHierarchy, Is.False);
        AssertFocused("first");
        for (int i = 0; i < 6; i++)
        {
            yield return KeyPress(Key.Tab);
            Assert.That(_stack.Top!.View.Contains(_host.focusController.focusedElement as VisualElement), Is.True);
        }
        yield return KeyPress(Key.Escape);
        AssertFocused("second");
        screen.View.Q<Button>("second").SetEnabled(false);
        _stack.PushModal(Menu());
        _stack.Pop();
        yield return Frames();
        AssertFocused("first"); // Invalidated return target falls back.
        _stack.PushModal(Menu());
        _stack.Dispose(); // Scheduled initial focus must be cancelled.
        yield return Frames();
        Assert.That(_host.childCount, Is.Zero);
        Assert.That(_blocked, Is.False);
    }

    [UnityTest]
    public IEnumerator ReopenAndReplaceDisposeEachLifetimeOnce()
    {
        for (int i = 0; i < 3; i++)
        {
            yield return KeyPress(Key.Escape);
            AssertFocused("first");
            yield return KeyPress(Key.Enter);
            yield return KeyPress(Key.Escape);
        }
        Assert.That(_activations, Is.EqualTo(3));
        Assert.That(_disposals, Is.EqualTo(3));
        _stack.PushScreen(Menu());
        _stack.ReplaceScreen(Menu());
        yield return Frames();
        AssertFocused("first");
        Assert.That(_stack.Count, Is.EqualTo(1));
        Assert.That(_disposals, Is.EqualTo(4));
    }

    [UnityTest]
    public IEnumerator GameplaySubmitDoesNotLeakThroughClosingMenu()
    {
        int gameplayCommands = 0;
        using (var fire = new InputAction("Fire", InputActionType.Button, "<Keyboard>/enter"))
        {
            fire.performed += _ =>
            {
                if (!_blocked)
                {
                    gameplayCommands++;
                }
            };
            fire.Enable();
            yield return KeyPress(Key.Escape);
            _stack.Top!.View.Q<Button>("first").clicked += () => _stack.Pop();
            yield return KeyPress(Key.Enter);
            Assert.That(_stack.Count, Is.Zero);
            Assert.That(gameplayCommands, Is.Zero, "Closing Submit must not become gameplay input");
            yield return KeyPress(Key.Enter);
            Assert.That(gameplayCommands, Is.EqualTo(1), "A new press after closing is gameplay input");
        }
    }

    [UnityTest]
    public IEnumerator CoveredScreensAndNestedModalsCannotReceiveFocus()
    {
        _stack.PushScreen(Menu());
        UiStackEntry first = _stack.Top!;
        _stack.PushScreen(Menu());
        yield return Frames();
        Assert.That(first.View.resolvedStyle.display, Is.EqualTo(DisplayStyle.None));
        _stack.PushModal(Menu());
        UiStackEntry lowerModal = _stack.Top!;
        _stack.PushModal(Menu());
        yield return Frames();
        Assert.That(lowerModal.View.enabledInHierarchy, Is.False);
        yield return PadPress(GamepadButton.DpadDown);
        Assert.That(_stack.Top!.View.Contains(_host.focusController.focusedElement as VisualElement), Is.True);
        yield return PadPress(GamepadButton.East);
        Assert.That(_stack.Top!, Is.SameAs(lowerModal));
        AssertFocused("first");
    }

    [UnityTest]
    public IEnumerator PointerActivationAndHiddenControlSkippingAreNative()
    {
        _stack.PushScreen(Menu());
        yield return Frames();
        _stack.Top!.View.Q<Button>("second").style.display = DisplayStyle.None;
        yield return Frames();
        yield return KeyPress(Key.DownArrow);
        AssertFocused("third");
        Button first = _stack.Top!.View.Q<Button>("first");
        Vector2 point = first.worldBound.center;
        Rect panelBounds = _host.panel.visualTree.worldBound;
        point = new Vector2(point.x * Screen.width / panelBounds.width,
            Screen.height - point.y * Screen.height / panelBounds.height);
        InputSystem.QueueStateEvent(_mouse, new MouseState { position = point });
        yield return Frames();
        InputSystem.QueueStateEvent(_mouse, new MouseState { position = point, buttons = 1 });
        yield return Frames();
        InputSystem.QueueStateEvent(_mouse, new MouseState { position = point });
        yield return Frames();
        Assert.That(_activations, Is.EqualTo(1));
        AssertFocused("first");
    }

    [UnityTest]
    public IEnumerator ChildCancelConsumptionAndPersistentRootAreRespected()
    {
        UiStackEntry menu = Menu();
        // This native-control boundary consumes Cancel before the stack's bubble callback.
        EventCallback<NavigationCancelEvent> consume = evt => evt.StopPropagation();
        menu.View.Q<Button>("first").RegisterCallback(consume);
        _stack.PushScreen(menu);
        yield return Frames();
        yield return KeyPress(Key.Escape);
        Assert.That(_stack.Count, Is.EqualTo(1));
        menu.View.Q<Button>("first").UnregisterCallback(consume);
        yield return KeyPress(Key.Escape);
        Assert.That(_stack.Count, Is.Zero);
        VisualElement view = new Button();
        _stack.PushScreen(new UiStackEntry(view, () => view,
            new Lifetime(() => _disposals++), dismissOnCancel: false));
        yield return Frames();
        yield return KeyPress(Key.Escape);
        Assert.That(_stack.Count, Is.EqualTo(1));
    }

    [UnityTest]
    public IEnumerator TeardownFailureStillReleasesAllEntriesAndGate()
    {
        _stack.PushScreen(Menu());
        UiStackEntry failing = new UiStackEntry(new VisualElement(), () => null,
            new Lifetime(() => throw new InvalidOperationException("fixture teardown")));
        _stack.PushModal(failing);
        Assert.Throws<AggregateException>(() => _stack.Dispose());
        Assert.That(_disposals, Is.EqualTo(1));
        Assert.That(_host.childCount, Is.Zero);
        Assert.That(_blocked, Is.False);
        _stack.Dispose();
        yield return Frames();
    }

    [UnityTest]
    public IEnumerator NativeRepeatStillMovesWhileHeld()
    {
        _stack.PushScreen(Menu());
        yield return Frames();
        int moves = 0;
        _host.RegisterCallback<NavigationMoveEvent>(_ => moves++);
        InputSystem.QueueStateEvent(_keyboard, new KeyboardState(Key.DownArrow));
        yield return Frames();
        AssertFocused("second");
        yield return new WaitForSecondsRealtime(0.9f);
        InputSystem.QueueStateEvent(_keyboard, new KeyboardState());
        yield return Frames();
        Assert.That(moves, Is.GreaterThan(1), "Do not suppress intentional hold repeat");
        Assert.That(_stack.Top!.View.Contains(_host.focusController.focusedElement as VisualElement), Is.True);
    }

    [UnityTest]
    public IEnumerator DuplicateRouterMutationIsDetected()
    {
        _stack.PushScreen(Menu());
        yield return Frames();
        // Deliberately add a raw input router before native UI dispatch.
        using (var duplicateMove = new InputAction("DuplicateMove", InputActionType.Button,
            "<Keyboard>/downArrow"))
        {
            duplicateMove.performed += _ => _stack.Top!.View.Q<Button>("second").Focus();
            duplicateMove.Enable();
            EventCallback<NavigationMoveEvent> stop = evt => evt.StopImmediatePropagation();
            _host.RegisterCallback(stop, TrickleDown.TrickleDown);
            yield return KeyPress(Key.DownArrow);
            Assert.Throws<AssertionException>(() => AssertFocused("second"),
                "The ordinary final-focus gate must reject the injected duplicate router");
            AssertFocused("third");
            _host.UnregisterCallback(stop, TrickleDown.TrickleDown);
        }
        _stack.Top!.View.Q<Button>("first").Focus();
        yield return KeyPress(Key.DownArrow);
        AssertFocused("second");
    }

    private UiStackEntry Menu()
    {
        VisualElement view = Resources.Load<VisualTreeAsset>("Menu").CloneTree().Q("menu");
        view.RemoveFromHierarchy();
        foreach (Button button in view.Query<Button>().ToList())
        {
            button.clicked += () => _activations++;
        }
        return new UiStackEntry(view, () => view.Q<Button>("first"),
            new Lifetime(() => _disposals++));
    }

    private string? FocusedName() => (_host.focusController.focusedElement as VisualElement)?.name;
    private void AssertFocused(string name) => Assert.That(FocusedName(), Is.EqualTo(name));

    private IEnumerator KeyPress(Key key)
    {
        InputSystem.QueueStateEvent(_keyboard, new KeyboardState(key));
        yield return Frames();
        InputSystem.QueueStateEvent(_keyboard, new KeyboardState());
        yield return Frames();
    }

    private IEnumerator PadPress(GamepadButton button)
    {
        InputSystem.QueueStateEvent(_gamepad, new GamepadState().WithButton(button));
        yield return Frames();
        InputSystem.QueueStateEvent(_gamepad, new GamepadState());
        yield return Frames();
    }

    private static IEnumerator Frames()
    {
        for (int i = 0; i < 6; i++)
        {
            yield return null;
        }
    }

    private sealed class Lifetime : IDisposable
    {
        private Action? _dispose;
        public Lifetime(Action dispose) => _dispose = dispose;
        public void Dispose()
        {
            Action? dispose = _dispose;
            _dispose = null;
            dispose?.Invoke();
        }
    }
}
