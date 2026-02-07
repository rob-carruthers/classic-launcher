import re
from dataclasses import dataclass
from typing import final


@dataclass(frozen=True)
class Category:
    name: str
    xdg_categories: frozenset[str]


@dataclass
class LauncherConfig:
    categories: frozenset[Category]


class LocalizedAttrsBase:
    match_ = ""

    def __init__(self, **kwargs: dict[str, str]):
        for k, v in kwargs.items():
            match = re.match(self.pattern, k)
            if not match:
                continue
            locale = match.groups()[0]
            setattr(self, locale, v)

    def __repr__(self) -> str:
        attrs = [f"{k}={v}" for k, v in sorted(self.__dict__.items())]
        attrs = ", ".join(attrs)
        return f"{type(self).__name__}({attrs})"

    @property
    def pattern(self) -> str:
        return rf"{self.match_}\[(.{{1,4}})\]"


class LocalizedNames(LocalizedAttrsBase):
    match_ = "name"


class LocalizedGenericNames(LocalizedAttrsBase):
    match_ = "genericname"


class LocalizedComments(LocalizedAttrsBase):
    match_ = "comment"


class Localizations:
    def __init__(
        self,
        names: LocalizedNames,
        genericnames: LocalizedGenericNames,
        comments: LocalizedComments,
    ):
        self.names = names
        self.genericnames = genericnames
        self.comments = comments


@final
class DesktopEntry:
    def __init__(
        self,
        type: str,  # noqa: A002
        name: str,
        version: str | None = None,
        genericname: str | None = None,
        nodisplay: bool | None = None,
        comment: str | None = None,
        icon: str | None = None,
        hidden: bool | None = None,
        onlyshowin: str | None = None,
        notshowin: str | None = None,
        dbusactivatable: bool | None = None,
        tryexec: str | None = None,
        exec: str | None = None,
        path: str | None = None,
        terminal: bool | None = None,
        actions: str | None = None,
        mimetype: str | None = None,
        categories: str | None = None,
        implements: str | None = None,
        keywords: str | None = None,
        startupnotify: bool | None = None,
        startupwmclass: str | None = None,
        url: str | None = None,
        prefersnondefaultgpu: bool | None = None,
        singlemainwindow: bool | None = None,
        **kwargs: dict[str, str],
    ):
        self.type = type
        self.name = name
        self.version = version
        self.genericname = genericname
        self.nodisplay = nodisplay
        self.comment = comment
        self.icon = icon
        self.hidden = hidden
        self._onlyshowin = None if onlyshowin is None else onlyshowin.rstrip(";")
        self._notshowin = None if notshowin is None else notshowin.rstrip(";")
        self.dbusactivatable = dbusactivatable
        self.tryexec = tryexec
        self.exec = exec
        self.path = path
        self.terminal = terminal
        self._actions = None if actions is None else actions.rstrip(";")
        self._mimetype = None if mimetype is None else mimetype.rstrip(";")
        self._categories = None if categories is None else categories.rstrip(";")
        self._implements = None if implements is None else implements.rstrip(";")
        self._keywords = None if keywords is None else keywords.rstrip(";")
        self.startupnotify = startupnotify
        self.startupwmclass = startupwmclass
        self.url = url
        self.prefersnondefaultgpu = prefersnondefaultgpu
        self.singlemainwindow = singlemainwindow

        localized_names_dict = {k: v for k, v in kwargs.items() if "name[" in k}
        localized_names = LocalizedNames(**localized_names_dict)
        for k in localized_names_dict:
            kwargs.pop(k)

        localized_genericnames_dict = {k: v for k, v in kwargs.items() if "name[" in k}
        localized_genericnames = LocalizedGenericNames(**localized_genericnames_dict)
        for k in localized_genericnames_dict:
            kwargs.pop(k)

        localized_comments_dict = {k: v for k, v in kwargs.items() if "comment[" in k}
        localized_comments = LocalizedComments(**localized_comments_dict)
        for k in localized_comments_dict:
            kwargs.pop(k)

        self.localizations = Localizations(
            localized_names,
            localized_genericnames,
            localized_comments,
        )

    def __repr__(self) -> str:
        attrs = [f"{attr}={getattr(self, attr)}" for attr in ("name", "exec", "type", "categories")]

        return f"DesktopEntry({', '.join(attrs)})"

    @property
    def onlyshowin(self) -> list[str] | None:
        return None if self._onlyshowin is None else self._onlyshowin.split(";")

    @property
    def notshowin(self) -> list[str] | None:
        return None if self._notshowin is None else self._notshowin.split(";")

    @property
    def actions(self) -> list[str] | None:
        return None if self._actions is None else self._actions.split(";")

    @property
    def mimetype(self) -> list[str] | None:
        return None if self._mimetype is None else self._mimetype.split(";")

    @property
    def categories(self) -> list[str] | None:
        return None if self._categories is None else self._categories.split(";")

    @property
    def implements(self) -> list[str] | None:
        return None if self._implements is None else self._implements.split(";")

    @property
    def keywords(self) -> list[str] | None:
        return None if self._keywords is None else self._keywords.split(";")
