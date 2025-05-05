from typing import List, NotRequired

from pydoll.protocol.base import CommandParams
from pydoll.protocol.input.types import (
    DragData,
    TouchPoint,
)
from pydoll.constants import (
    DragEventType,
    KeyEventType,
    KeyLocation,
    KeyModifier,
    MouseButton,
    MouseEventType,
    PointerType,
    TouchEventType,
    GestureSourceType,
)


class DispatchKeyEventParams(CommandParams):
    type: KeyEventType
    modifiers: NotRequired[KeyModifier]
    timestamp: NotRequired[float]
    text: NotRequired[str]
    unmodifiedText: NotRequired[str]
    keyIdentifier: NotRequired[str]
    code: NotRequired[str]
    key: NotRequired[str]
    windowsVirtualKeyCode: NotRequired[int]
    nativeVirtualKeyCode: NotRequired[int]
    autoRepeat: NotRequired[bool]
    isKeypad: NotRequired[bool]
    isSystemKey: NotRequired[bool]
    location: NotRequired[KeyLocation]
    commands: NotRequired[List[str]]


class DispatchMouseEventParams(CommandParams):
    type: MouseEventType
    x: int
    y: int
    modifiers: NotRequired[KeyModifier]
    timestamp: NotRequired[float]
    button: NotRequired[MouseButton]
    clickCount: NotRequired[int]
    force: NotRequired[float]
    tangentialPressure: NotRequired[float]
    tiltX: NotRequired[float]
    tiltY: NotRequired[float]
    twist: NotRequired[int]
    deltaX: NotRequired[float]
    deltaY: NotRequired[float]
    pointerType: NotRequired[PointerType]


class DispatchTouchEventParams(CommandParams):
    type: TouchEventType
    touchPoints: NotRequired[List[TouchPoint]]
    modifiers: NotRequired[KeyModifier]
    timestamp: NotRequired[float]


class SetIgnoreInputEventsParams(CommandParams):
    enabled: bool


class DispatchDragEventParams(CommandParams):
    type: DragEventType
    x: int
    y: int
    data: NotRequired[DragData]
    modifiers: NotRequired[KeyModifier]


class EmulateTouchFromMouseEventParams(CommandParams):
    type: MouseEventType
    x: int
    y: int
    button: MouseButton
    timestamp: NotRequired[float]
    deltaX: NotRequired[float]
    deltaY: NotRequired[float]
    modifiers: NotRequired[KeyModifier]
    clickCount: NotRequired[int]


class ImeSetCompositionParams(CommandParams):
    text: str
    selectionStart: int
    selectionEnd: int
    replacementStart: NotRequired[int]
    replacementEnd: NotRequired[int]


class InsertTextParams(CommandParams):
    text: str


class SetInterceptDragsParams(CommandParams):
    enabled: bool


class SynthesizePinchGestureParams(CommandParams):
    x: int
    y: int
    scaleFactor: float
    relativeSpeed: NotRequired[float]
    gestureSourceType: NotRequired[GestureSourceType]


class SynthesizeScrollGestureParams(CommandParams):
    x: int
    y: int
    xDistance: NotRequired[float]
    yDistance: NotRequired[float]
    xOverscroll: NotRequired[float]
    yOverscroll: NotRequired[float]
    preventFling: NotRequired[bool]
    speed: NotRequired[int]
    gestureSourceType: NotRequired[GestureSourceType]
    repeatCount: NotRequired[int]
    repeatDelayMs: NotRequired[int]
    interactionMarkerName: NotRequired[str]


class SynthesizeTapGestureParams(CommandParams):
    x: int
    y: int
    duration: NotRequired[int]
    tapCount: NotRequired[int]
    gestureSourceType: NotRequired[GestureSourceType]
