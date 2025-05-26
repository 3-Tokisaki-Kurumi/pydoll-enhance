from typing import List, NotRequired, TypedDict

from pydoll.constants import (
    OriginTrialStatus,
    OriginTrialTokenStatus,
    OriginTrialUsageRestriction,
    PermissionsPolicyBlockReason,
    PermissionsPolicyFeature,
    ResourceType,
    TransitionType,
)


class Viewport(TypedDict):
    """Viewport for capturing screenshot or clip rectangle."""

    x: float
    y: float
    width: float
    height: float
    scale: NotRequired[float]


class InstallabilityErrorArgument(TypedDict):
    name: str
    value: str


class InstallabilityError(TypedDict):
    errorId: str
    errorArguments: List[InstallabilityErrorArgument]


class FontFamilies(TypedDict):
    standard: NotRequired[str]
    fixed: NotRequired[str]
    serif: NotRequired[str]
    sansSerif: NotRequired[str]
    cursive: NotRequired[str]
    fantasy: NotRequired[str]
    math: NotRequired[str]


class ScriptFontFamilies(TypedDict):
    script: str
    fontFamilies: FontFamilies


class FontSizes(TypedDict):
    standard: NotRequired[int]
    fixed: NotRequired[int]


class AppManifestError(TypedDict):
    """App manifest error structure."""

    message: str
    critical: NotRequired[int]
    line: NotRequired[int]
    column: NotRequired[int]


class ImageResource(TypedDict):
    url: str
    sizes: NotRequired[str]
    type: NotRequired[str]


class FileFilter(TypedDict):
    name: NotRequired[str]
    accepts: NotRequired[List[str]]


class FileHandler(TypedDict):
    action: str
    name: str
    icons: NotRequired[List[ImageResource]]
    accepts: NotRequired[List[FileFilter]]
    launchType: NotRequired[str]


class LaunchHandler(TypedDict):
    clientMode: str


class ProtocolHandler(TypedDict):
    protocol: str
    url: str


class RelatedApplication(TypedDict):
    id: str
    url: str


class ScopeExtension(TypedDict):
    origin: str
    hasOriginWildcard: bool


class Screenshot(TypedDict):
    image: ImageResource
    formFactor: str
    label: NotRequired[str]


class ShareTarget(TypedDict):
    action: str
    method: str
    enctype: str
    title: NotRequired[str]
    text: NotRequired[str]
    url: NotRequired[str]
    files: NotRequired[List[FileFilter]]


class Shortcut(TypedDict):
    name: str
    url: str


class WebAppManifest(TypedDict):
    backgroundColor: NotRequired[str]
    description: NotRequired[str]
    dir: NotRequired[str]
    display: NotRequired[str]
    displayOverrides: NotRequired[List[str]]
    fileHandlers: NotRequired[List[FileHandler]]
    icons: NotRequired[List[ImageResource]]
    id: NotRequired[str]
    lang: NotRequired[str]
    launchHandler: NotRequired[LaunchHandler]
    name: NotRequired[str]
    orientation: NotRequired[str]
    preferRelatedApplications: NotRequired[bool]
    protocolHandlers: NotRequired[List[ProtocolHandler]]
    relatedApplications: NotRequired[List[RelatedApplication]]
    scope: NotRequired[str]
    scopeExtensions: NotRequired[List[ScopeExtension]]
    screenshots: NotRequired[List[Screenshot]]
    shareTarget: NotRequired[ShareTarget]
    shortName: NotRequired[str]
    shortcuts: NotRequired[List[Shortcut]]
    startUrl: NotRequired[str]
    themeColor: NotRequired[str]


class Frame(TypedDict):
    """Information about a frame."""

    id: str
    loaderId: NotRequired[str]
    url: str
    securityOrigin: NotRequired[str]
    mimeType: NotRequired[str]
    unreachableUrl: NotRequired[str]


class FrameResource(TypedDict):
    url: str
    type: ResourceType
    mimeType: str
    lastModified: NotRequired[str]
    contentSize: NotRequired[float]
    failed: NotRequired[bool]
    canceled: NotRequired[bool]


class FrameResourceTree(TypedDict):
    """Information about frame hierarchy."""

    frame: Frame
    childFrames: NotRequired[List['FrameResourceTree']]
    resources: NotRequired[List[FrameResource]]


class FrameTree(TypedDict):
    frame: Frame
    childFrames: NotRequired[List['FrameTree']]


class LayoutViewport(TypedDict):
    """Layout viewport position and dimensions."""

    pageX: int
    pageY: int
    clientWidth: int
    clientHeight: int


class VisualViewport(TypedDict):
    """Visual viewport position, dimensions, and scale."""

    offsetX: float
    offsetY: float
    pageX: float
    pageY: float
    clientWidth: float
    clientHeight: float
    scale: float
    zoom: NotRequired[float]


class NavigationEntry(TypedDict):
    """Navigation history entry."""

    id: int
    url: str
    userTypedURL: str
    title: str
    transitionType: TransitionType


class AdScriptId(TypedDict):
    scriptId: str
    debuggerId: str


class OriginTrialToken(TypedDict):
    origin: str
    matchSubDomains: bool
    trialName: str
    expiryTime: str
    isThirdParty: bool
    usageRestriction: NotRequired[OriginTrialUsageRestriction]


class OriginTrialTokenWithStatus(TypedDict):
    rawTokenText: str
    parsedTokenText: NotRequired[OriginTrialToken]
    status: OriginTrialTokenStatus


class OriginTrial(TypedDict):
    trialName: str
    status: OriginTrialStatus
    tokenWithStatus: List[OriginTrialTokenWithStatus]


class PermissionsPolicyBlockLocator(TypedDict):
    frameId: str
    blockReason: PermissionsPolicyBlockReason


class PermissionsPolicyFeatureState(TypedDict):
    feature: PermissionsPolicyFeature
    allowed: bool
    locator: NotRequired[PermissionsPolicyBlockLocator]
