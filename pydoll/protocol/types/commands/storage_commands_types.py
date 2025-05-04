from typing import List, NotRequired, TypedDict

from pydoll.protocol.types.commands import CommandParams
from pydoll.protocol.types.commands.network_commands_types import CookieParam


class StorageBucket(TypedDict):
    storageKey: str
    name: NotRequired[str]


class RelatedWebsiteSet(TypedDict):
    primarySites: List[str]
    associatedSites: List[str]
    serviceSites: List[str]


class ClearCookiesParams(CommandParams):
    browserContextId: NotRequired[str]


class ClearDataForOriginParams(CommandParams):
    origin: str
    storageTypes: str


class ClearDataForStorageKeyParams(CommandParams):
    storageKey: str
    storageTypes: str


class GetCookiesParams(CommandParams):
    browserContextId: NotRequired[str]


class GetStorageKeyForFrameParams(CommandParams):
    frameId: str


class GetUsageAndQuotaParams(CommandParams):
    origin: str


class SetCookiesParams(CommandParams):
    cookies: List[CookieParam]
    browserContextId: NotRequired[str]


class SetProtectedAudienceKAnonymityParams(CommandParams):
    owner: str
    name: str
    hashes: List[str]


class TrackCacheStorageForOriginParams(CommandParams):
    origin: str


class TrackCacheStorageForStorageKeyParams(CommandParams):
    storageKey: str


class TrackIndexedDBForOriginParams(CommandParams):
    origin: str


class TrackIndexedDBForStorageKeyParams(CommandParams):
    storageKey: str


class UntrackCacheStorageForOriginParams(CommandParams):
    origin: str


class UntrackCacheStorageForStorageKeyParams(CommandParams):
    storageKey: str


class UntrackIndexedDBForOriginParams(CommandParams):
    origin: str


class UntrackIndexedDBForStorageKeyParams(CommandParams):
    storageKey: str


class ClearSharedStorageEntriesParams(CommandParams):
    ownerOrigin: str


class ClearTrustTokensParams(CommandParams):
    issuerOrigin: str


class DeleteSharedStorageEntryParams(CommandParams):
    ownerOrigin: str
    key: str


class DeleteStorageBucketParams(CommandParams):
    bucket: StorageBucket


class GetAffectedUrlsForThirdPartyCookieMetadataParams(CommandParams):
    firstPartyUrl: str
    thirdPartyUrls: List[str]


class GetInterestGroupDetailsParams(CommandParams):
    ownerOrigin: str
    name: str


class GetRelatedWebsiteSetsParams(CommandParams):
    sets: List[RelatedWebsiteSet]


class GetSharedStorageEntriesParams(CommandParams):
    ownerOrigin: str


class GetSharedStorageMetadataParams(CommandParams):
    ownerOrigin: str


class OverrideQuotaForOriginParams(CommandParams):
    origin: str
    quotaSize: NotRequired[float]


class ResetSharedStorageBudgetParams(CommandParams):
    ownerOrigin: str


class SetAttributionReportingLocalTestingModeParams(CommandParams):
    enable: bool


class SetAttributionReportingTrackingParams(CommandParams):
    enable: bool


class SetInterestGroupAuctionTrackingParams(CommandParams):
    enable: bool


class SetInterestGroupTrackingParams(CommandParams):
    enable: bool


class SetSharedStorageEntryParams(CommandParams):
    ownerOrigin: str
    key: str
    value: str
    ignoreIfPresent: NotRequired[bool]


class SetSharedStorageTrackingParams(CommandParams):
    enable: bool


class SetStorageBucketTrackingParams(CommandParams):
    storageKey: str
    enable: bool
