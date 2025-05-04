from typing import List, NotRequired, TypedDict

from pydoll.constants import WindowState
from pydoll.protocol.types.commands import CommandParams


class RemoteLocation(TypedDict):
    host: str
    port: int


class ActivateTargetParams(CommandParams):
    targetId: str


class AttachToTargetParams(CommandParams):
    targetId: str
    flatten: NotRequired[bool]


class CloseTargetParams(CommandParams):
    targetId: str


class CreateBrowserContextParams(CommandParams):
    disposeOnDetach: NotRequired[bool]
    proxyServer: NotRequired[str]
    proxyBypassList: NotRequired[str]
    originsWithUniversalNetworkAccess: NotRequired[List[str]]


class CreateTargetParams(CommandParams):
    url: str
    left: NotRequired[int]
    top: NotRequired[int]
    width: NotRequired[int]
    height: NotRequired[int]
    windowState: NotRequired[WindowState]
    browserContextId: NotRequired[str]
    enableBeginFrameControl: NotRequired[bool]
    newWindow: NotRequired[bool]
    background: NotRequired[bool]
    forTab: NotRequired[bool]
    hidden: NotRequired[bool]


class DetachFromTargetParams(CommandParams):
    sessionId: NotRequired[str]


class DisposeBrowserContextParams(CommandParams):
    browserContextId: str


class GetTargetsParams(CommandParams):
    filter: NotRequired[List]


class SetAutoAttachParams(CommandParams):
    autoAttach: bool
    waitForDebuggerOnStart: NotRequired[bool]
    flatten: NotRequired[bool]
    filter: NotRequired[List]


class SetDiscoverTargetsParams(CommandParams):
    discover: bool
    filter: NotRequired[List]


class AttachToBrowserTargetParams(CommandParams):
    sessionId: str


class AutoAttachRelatedParams(CommandParams):
    targetId: str
    waitForDebuggerOnStart: NotRequired[bool]
    filter: NotRequired[List]


class ExposeDevToolsProtocolParams(CommandParams):
    targetId: str
    bindingName: NotRequired[str]
    inherintPermissions: NotRequired[bool]


class GetTargetInfoParams(CommandParams):
    targetId: str


class SetRemoteLocationsParams(CommandParams):
    locations: List[RemoteLocation]
