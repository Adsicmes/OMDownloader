# coding:utf-8

from typing import List

import PySide6
import i18n
from PySide6.QtCore import Qt, Signal, QMargins
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QButtonGroup, \
    QFrame
from loguru import logger
from qfluentwidgets import LineEdit, ComboBox, RadioButton, CheckBox, FlowLayout, \
    PrimaryPushButton, TextEdit, ScrollArea, DoubleSpinBox, DatePicker, ZhDatePicker, SpinBox, ToolTipFilter, \
    ToolTipPosition

from packages.config import config
from packages.enums import Mirrors
from packages.enums.search_params_in_official import *
from packages.model import DownloadParams, DownloadParamsOfficial, DownloadParamsFilter


class BatchDownloadSubInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("BatchDownloadSubInterface")
        self.initWidget()
        self.initLayout()

    def initWidget(self):
        self.paramWidget = ParamFillInWidget(self)

        self.statusLabel = TextEdit()
        self.statusLabel.setEnabled(False)
        self.statusLabel.setMarkdown(i18n.t("app.mapDownloadPage.batchDownloadPage.statusLabel"))

        self.sortLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.sort"), self)
        self.sortComboBox = ComboBox(self)
        self.sortComboBox.addItems(
            [i18n.t(f"app.mapDownloadPage.batchDownloadPage.sort.{i.value}") for i in ParamsSort])
        self.sortComboBox.setCurrentIndex(7)  # ranked reverse
        self.sortComboBox.setFixedWidth(175)
        self.countLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.count"), self)
        self.countSpinBox = SpinBox(self)
        self.countSpinBox.setMaximum(10000)
        self.countSpinBox.setValue(200)
        self.countSpinBox.setFixedWidth(175)
        self.mirrorLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.mirror"), self)
        self.mirrorComboBox = ComboBox(self)
        self.mirrorComboBox.addItems([i.value for i in Mirrors])
        self.mirrorComboBox.setCurrentIndex(0)
        self.mirrorComboBox.setFixedWidth(175)

        self.execButton = PrimaryPushButton(self)
        self.execButton.clicked.connect(self._onExecButtonClicked)

        self.execButton.setText(i18n.t("app.mapDownloadPage.batchDownloadPage.execButton"))

    def initLayout(self):
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(10, 10, 5, 5)
        self.hBoxLayout.setSpacing(10)

        self.scrollArea = ScrollArea(self)
        self.scrollArea.setWidget(self.paramWidget)
        self.scrollArea.setFrameShape(QFrame.NoFrame)  # noqa
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.ensureWidgetVisible(self.paramWidget)
        self.scrollArea.verticalScrollBar().setValue(0)

        self.sortHBoxLayout = QHBoxLayout()
        self.countHBoxLayout = QHBoxLayout()
        self.mirrorHBoxLayout = QHBoxLayout()

        self.sortHBoxLayout.addWidget(self.sortLabel)
        self.sortHBoxLayout.addWidget(self.sortComboBox)
        self.countHBoxLayout.addWidget(self.countLabel)
        self.countHBoxLayout.addWidget(self.countSpinBox)
        self.mirrorHBoxLayout.addWidget(self.mirrorLabel)
        self.mirrorHBoxLayout.addWidget(self.mirrorComboBox)

        self.leftVBoxLayout = QVBoxLayout()
        self.rightVBoxLayout = QVBoxLayout()
        self.rightVBoxLayout.setContentsMargins(5, 10, 0, 0)
        self.rightVBoxLayout.setSpacing(30)

        self.statusLabel.setFixedWidth(300)

        self.leftVBoxLayout.addWidget(self.scrollArea)
        self.rightVBoxLayout.addWidget(self.statusLabel, Qt.AlignmentFlag.AlignTop)
        self.rightVBoxLayout.addLayout(self.sortHBoxLayout)
        self.rightVBoxLayout.addLayout(self.countHBoxLayout)
        self.rightVBoxLayout.addLayout(self.mirrorHBoxLayout)
        self.rightVBoxLayout.addWidget(self.execButton, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        # self.hBoxLayout.addWidget(self.paramWidget)
        self.hBoxLayout.addLayout(self.leftVBoxLayout)
        self.hBoxLayout.addLayout(self.rightVBoxLayout)

    def getParams(self) -> DownloadParams:
        if self.paramWidget.cEnabled.isChecked():
            indexes = self.paramWidget.cCheckboxWidget.getSelectedButtonIndexes()
            print(indexes)
            c = []
            for i in indexes:
                match i:
                    case 0:
                        c.append(ParamsC.Recommended)
                    case 1:
                        c.append(ParamsC.ConvertMapIncluded)
                    case 2:
                        c.append(ParamsC.FollowMappers)
                    case 3:
                        c.append(ParamsC.SpotlightMaps)
                    case 4:
                        c.append(ParamsC.FeaturedArtists)
        else:
            c = None

        if self.paramWidget.mEnabled.isChecked():
            index = self.paramWidget.mRadioWidget.getActivatedButtonIndex()
            match index:
                case 0:
                    m = ParamsM.Std
                case 1:
                    m = ParamsM.Taiko
                case 2:
                    m = ParamsM.Catch
                case 3:
                    m = ParamsM.Mania
                case _:
                    m = None
        else:
            m = None

        if self.paramWidget.sEnabled.isChecked():
            index = self.paramWidget.sRadioWidget.getActivatedButtonIndex()
            match index:
                case 0:
                    s = ParamsS.Any
                case 1:
                    s = ParamsS.Ranked
                case 2:
                    s = ParamsS.Qualified
                case 3:
                    s = ParamsS.Loved
                case 4:
                    s = ParamsS.Favourites
                case 5:
                    s = ParamsS.Pending
                case 6:
                    s = ParamsS.Wip
                case 7:
                    s = ParamsS.Graveyard
                case 8:
                    s = ParamsS.Mine
                case _:
                    s = None
        else:
            s = None

        if self.paramWidget.nsfwEnabled.isChecked():
            index = self.paramWidget.nsfwRadioWidget.getActivatedButtonIndex()
            match index:
                case 0:
                    nsfw = ParamsNsfw.Excluded
                case 1:
                    nsfw = ParamsNsfw.Included
                case _:
                    nsfw = None
        else:
            nsfw = None

        if self.paramWidget.eEnabled.isChecked():
            indexes = self.paramWidget.eCheckboxWidget.getSelectedButtonIndexes()
            e = []
            for i in indexes:
                match i:
                    case 0:
                        e.append(ParamsE.Video)
                    case 1:
                        e.append(ParamsE.Storyboard)
        else:
            e = None

        if self.paramWidget.rEnabled.isChecked():
            indexes = self.paramWidget.rCheckboxWidget.getSelectedButtonIndexes()
            r = []
            for i in indexes:
                match i:
                    case 0:
                        r.append(ParamsR.XH)
                    case 1:
                        r.append(ParamsR.X)
                    case 2:
                        r.append(ParamsR.SH)
                    case 3:
                        r.append(ParamsR.S)
                    case 4:
                        r.append(ParamsR.A)
                    case 5:
                        r.append(ParamsR.B)
                    case 6:
                        r.append(ParamsR.C)
                    case 7:
                        r.append(ParamsR.D)
        else:
            r = None

        if self.paramWidget.playedEnabled.isChecked():
            played = self.paramWidget.playedRadioWidget.getActivatedButtonIndex()
            match played:
                case 0:
                    played = ParamsPlayed.Played
                case 1:
                    played = ParamsPlayed.Unplayed
                case _:
                    played = None
        else:
            played = None

        if self.paramWidget.lEnabled.isChecked():
            l = self.paramWidget.lRadioWidget.getActivatedButtonIndex()
            match l:
                case 0:
                    l = ParamsL.Unspecified
                case 1:
                    l = ParamsL.English
                case 2:
                    l = ParamsL.Japanese
                case 3:
                    l = ParamsL.Chinese
                case 4:
                    l = ParamsL.Instrumental
                case 5:
                    l = ParamsL.Korean
                case 6:
                    l = ParamsL.French
                case 7:
                    l = ParamsL.Germany
                case 8:
                    l = ParamsL.Swedish
                case 9:
                    l = ParamsL.Spanish
                case 10:
                    l = ParamsL.Italian
                case 11:
                    l = ParamsL.Russian
                case 12:
                    l = ParamsL.Polish
                case 13:
                    l = ParamsL.Others
                case _:
                    l = None
        else:
            l = None

        if self.paramWidget.gEnabled.isChecked():
            g = self.paramWidget.gRadioWidget.getActivatedButtonIndex()
            match g:
                case 0:
                    g = ParamsG.Unspecified
                case 1:
                    g = ParamsG.VideoGame
                case 2:
                    g = ParamsG.Anime
                case 3:
                    g = ParamsG.Rock
                case 4:
                    g = ParamsG.Pop
                case 5:
                    g = ParamsG.Others
                case 6:
                    g = ParamsG.Novelty
                case 7:
                    g = ParamsG.HipHop
                case 8:
                    g = ParamsG.Electronic
                case 9:
                    g = ParamsG.Metal
                case 10:
                    g = ParamsG.Classical
                case 11:
                    g = ParamsG.Folk
                case 12:
                    g = ParamsG.Jazz
                case _:
                    g = None
        else:
            g = None

        index = self.sortComboBox.currentIndex()
        match index:
            case 0:
                sort = ParamsSort.Title
            case 1:
                sort = ParamsSort.TitleReverse
            case 2:
                sort = ParamsSort.Artist
            case 3:
                sort = ParamsSort.ArtistReverse
            case 4:
                sort = ParamsSort.Difficulty
            case 5:
                sort = ParamsSort.DifficultyReverse
            case 6:
                sort = ParamsSort.Ranked
            case 7:
                sort = ParamsSort.RankedReverse
            case 8:
                sort = ParamsSort.Rating
            case 9:
                sort = ParamsSort.RatingReverse
            case 10:
                sort = ParamsSort.Plays
            case 11:
                sort = ParamsSort.PlaysReverse
            case 12:
                sort = ParamsSort.Favourites
            case 13:
                sort = ParamsSort.FavouritesReverse
            case _:
                sort = ParamsSort.RankedReverse

        index = self.mirrorComboBox.currentIndex()
        match index:
            case 0:
                mirror = Mirrors.Official
            case _:
                mirror = Mirrors.Official

        params = DownloadParams(
            official=DownloadParamsOfficial(
                q=self.paramWidget.qLineEdit.text(),
                c=c,
                m=m,
                s=s,
                nsfw=nsfw,
                e=e,
                r=r,
                played=played,
                l=l,
                g=g,
                sort=sort
            ),
            filter=DownloadParamsFilter(
                ar=self.paramWidget.arRangeWidget.getRange() if self.paramWidget.arEnabled.isChecked() else None,
                od=self.paramWidget.odRangeWidget.getRange() if self.paramWidget.odEnabled.isChecked() else None,
                cs=self.paramWidget.csRangeWidget.getRange() if self.paramWidget.csEnabled.isChecked() else None,
                hp=self.paramWidget.hpRangeWidget.getRange() if self.paramWidget.hpEnabled.isChecked() else None,
                bpm=self.paramWidget.bpmRangeWidget.getRange() if self.paramWidget.bpmEnabled.isChecked() else None,
                star=self.paramWidget.starRangeWidget.getRange() if self.paramWidget.starEnabled.isChecked() else None,
                length=self.paramWidget.lengthRangeWidget.getRange() if self.paramWidget.lengthEnabled.isChecked() else None,
                ranked=self.paramWidget.rankedRangeWidget.getRange() if self.paramWidget.rankedEnabled.isChecked() else None,
                created=self.paramWidget.createdRangeWidget.getRange() if self.paramWidget.createdEnabled.isChecked() else None,
            ),
            count=self.countSpinBox.value(),
            mirror=mirror
        )
        return params

    def _onExecButtonClicked(self):
        params = self.getParams()
        # TODO: Add task in handlers folder and call it with param.


class ParamFillInWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initWidget()
        self.initLayout()

    def initWidget(self):
        self.qLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.q"), self)
        self.qLabel.installEventFilter(ToolTipFilter(self.qLabel, 300, ToolTipPosition.TOP))
        self.qLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.qLabel"))
        self.qLineEdit = LineEdit(self)

        self.cEnabled = CheckBox("", self)
        self.cLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.c"), self)
        self.cLabel.installEventFilter(ToolTipFilter(self.cLabel, 300, ToolTipPosition.TOP))
        self.cLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.cLabel"))
        self.cCheckboxWidget = HCheckboxWidget(self)
        self.cCheckboxWidget.addItems([
            i18n.t("app.mapDownloadPage.batchDownloadPage.c.recommended"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.c.converts"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.c.follows"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.c.spotlights"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.c.featured_artists"),
        ])

        self.mEnabled = CheckBox("", self)
        self.mLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.m"), self)
        self.mLabel.installEventFilter(ToolTipFilter(self.mLabel, 300, ToolTipPosition.TOP))
        self.mLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.mLabel"))
        self.mRadioWidget = HRadioWidget(self)
        self.mRadioWidget.addItems([
            i18n.t("app.mapDownloadPage.batchDownloadPage.m.std"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.m.taiko"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.m.catch"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.m.mania"),
        ])

        self.sEnabled = CheckBox("", self)
        self.sLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.s"), self)
        self.sLabel.installEventFilter(ToolTipFilter(self.sLabel, 300, ToolTipPosition.TOP))
        self.sLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.sLabel"))
        self.sRadioWidget = HRadioWidget(self)
        self.sRadioWidget.addItems([
            i18n.t("app.mapDownloadPage.batchDownloadPage.s.any"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.s.ranked"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.s.qualified"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.s.loved"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.s.favourites"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.s.pending"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.s.wip"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.s.graveyard"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.s.mine"),
        ])

        self.nsfwEnabled = CheckBox("", self)
        self.nsfwLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.nsfw"), self)
        self.nsfwLabel.installEventFilter(ToolTipFilter(self.nsfwLabel, 300, ToolTipPosition.TOP))
        self.nsfwLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.nsfwLabel"))
        self.nsfwRadioWidget = HRadioWidget(self)
        self.nsfwRadioWidget.addItems([
            i18n.t("app.mapDownloadPage.batchDownloadPage.nsfw.off"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.nsfw.on"),
        ])

        self.eEnabled = CheckBox("", self)
        self.eLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.e"), self)
        self.eLabel.installEventFilter(ToolTipFilter(self.eLabel, 300, ToolTipPosition.TOP))
        self.eLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.eLabel"))
        self.eCheckboxWidget = HCheckboxWidget(self)
        self.eCheckboxWidget.addItems([
            i18n.t("app.mapDownloadPage.batchDownloadPage.e.video"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.e.storyboard"),
        ])

        self.rEnabled = CheckBox("", self)
        self.rLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.r"), self)
        self.rLabel.installEventFilter(ToolTipFilter(self.rLabel, 300, ToolTipPosition.TOP))
        self.rLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.rLabel"))
        self.rCheckboxWidget = HCheckboxWidget(self)
        self.rCheckboxWidget.addItems([
            i18n.t("app.mapDownloadPage.batchDownloadPage.r.XH"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.r.H"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.r.SH"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.r.S"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.r.A"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.r.B"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.r.C"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.r.D"),
        ])

        self.playedEnabled = CheckBox("", self)
        self.playedLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.played"), self)
        self.playedLabel.installEventFilter(ToolTipFilter(self.playedLabel, 300, ToolTipPosition.TOP))
        self.playedLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.playedLabel"))
        self.playedRadioWidget = HRadioWidget(self)
        self.playedRadioWidget.addItems([
            i18n.t("app.mapDownloadPage.batchDownloadPage.played.played"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.played.unplayed"),
        ])

        self.lEnabled = CheckBox("", self)
        self.lLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.l"), self)
        self.lLabel.installEventFilter(ToolTipFilter(self.lLabel, 300, ToolTipPosition.TOP))
        self.lLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.lLabel"))
        self.lRadioWidget = HRadioWidget(self)
        self.lRadioWidget.addItems([
            i18n.t("app.mapDownloadPage.batchDownloadPage.l.unspecified"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.l.english"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.l.japanese"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.l.chinese"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.l.instrumental"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.l.korean"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.l.french"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.l.germany"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.l.swedish"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.l.spanish"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.l.italian"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.l.russian"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.l.polish"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.l.others"),
        ])

        self.gEnabled = CheckBox("", self)
        self.gLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.g"), self)
        self.gLabel.installEventFilter(ToolTipFilter(self.gLabel, 300, ToolTipPosition.TOP))
        self.gLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.gLabel"))
        self.gRadioWidget = HRadioWidget(self)
        self.gRadioWidget.addItems([
            i18n.t("app.mapDownloadPage.batchDownloadPage.g.unspecified"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.g.videoGame"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.g.anime"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.g.rock"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.g.pop"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.g.others"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.g.novelty"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.g.hiphop"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.g.electronic"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.g.metal"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.g.classical"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.g.folk"),
            i18n.t("app.mapDownloadPage.batchDownloadPage.g.jazz"),
        ])

        self.arEnabled = CheckBox("", self)
        self.arLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.ar"), self)
        self.arLabel.installEventFilter(ToolTipFilter(self.arLabel, 300, ToolTipPosition.TOP))
        self.arLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.arLabel"))
        self.arRangeWidget = NumRangeUnit(self)

        self.odEnabled = CheckBox("", self)
        self.odLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.od"), self)
        self.odLabel.installEventFilter(ToolTipFilter(self.odLabel, 300, ToolTipPosition.TOP))
        self.odLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.odLabel"))
        self.odRangeWidget = NumRangeUnit(self)

        self.csEnabled = CheckBox("", self)
        self.csLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.cs"), self)
        self.csLabel.installEventFilter(ToolTipFilter(self.csLabel, 300, ToolTipPosition.TOP))
        self.csLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.csLabel"))
        self.csRangeWidget = NumRangeUnit(self)

        self.hpEnabled = CheckBox("", self)
        self.hpLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.hp"), self)
        self.hpLabel.installEventFilter(ToolTipFilter(self.hpLabel, 300, ToolTipPosition.TOP))
        self.hpLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.hpLabel"))
        self.hpRangeWidget = NumRangeUnit(self)

        self.bpmEnabled = CheckBox("", self)
        self.bpmLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.bpm"), self)
        self.bpmLabel.installEventFilter(ToolTipFilter(self.bpmLabel, 300, ToolTipPosition.TOP))
        self.bpmLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.bpmLabel"))
        self.bpmRangeWidget = NumRangeUnit(self)

        self.starEnabled = CheckBox("", self)
        self.starLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.star"), self)
        self.starLabel.installEventFilter(ToolTipFilter(self.starLabel, 300, ToolTipPosition.TOP))
        self.starLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.starLabel"))
        self.starRangeWidget = NumRangeUnit(self)

        self.lengthEnabled = CheckBox("", self)
        self.lengthLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.length"), self)
        self.lengthLabel.installEventFilter(ToolTipFilter(self.lengthLabel, 300, ToolTipPosition.TOP))
        self.lengthLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.lengthLabel"))
        self.lengthRangeWidget = NumRangeUnit(self)

        self.rankedEnabled = CheckBox("", self)
        self.rankedLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.ranked"), self)
        self.rankedLabel.installEventFilter(ToolTipFilter(self.rankedLabel, 300, ToolTipPosition.TOP))
        self.rankedLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.rankedLabel"))
        self.rankedRangeWidget = DateRangeUnit(self)

        self.createdEnabled = CheckBox("", self)
        self.createdLabel = QLabel(i18n.t("app.mapDownloadPage.batchDownloadPage.labels.created"), self)
        self.createdLabel.installEventFilter(ToolTipFilter(self.createdLabel, 300, ToolTipPosition.TOP))
        self.createdLabel.setToolTip(i18n.t("app.mapDownloadPage.batchDownloadPage.tooltip.createdLabel"))
        self.createdRangeWidget = DateRangeUnit(self)

    def initLayout(self):
        # TODO: Layout重构，除了搜索框之外的参数填写行，全部抽象为一个QWidget子类
        self.qLayout = QHBoxLayout()
        self.cLayout = QHBoxLayout()
        self.mLayout = QHBoxLayout()
        self.sLayout = QHBoxLayout()
        self.nsfwLayout = QHBoxLayout()
        self.eLayout = QHBoxLayout()
        self.rLayout = QHBoxLayout()
        self.playedLayout = QHBoxLayout()
        self.lLayout = QHBoxLayout()
        self.gLayout = QHBoxLayout()
        self.arLayout = QHBoxLayout()
        self.odLayout = QHBoxLayout()
        self.csLayout = QHBoxLayout()
        self.hpLayout = QHBoxLayout()
        self.bpmLayout = QHBoxLayout()
        self.starLayout = QHBoxLayout()
        self.lengthLayout = QHBoxLayout()
        self.rankedLayout = QHBoxLayout()
        self.createdLayout = QHBoxLayout()

        layoutMargin = QMargins(5, 10, 15, 10)
        self.qLayout.setContentsMargins(layoutMargin)
        self.cLayout.setContentsMargins(layoutMargin)
        self.mLayout.setContentsMargins(layoutMargin)
        self.sLayout.setContentsMargins(layoutMargin)
        self.nsfwLayout.setContentsMargins(layoutMargin)
        self.eLayout.setContentsMargins(layoutMargin)
        self.rLayout.setContentsMargins(layoutMargin)
        self.playedLayout.setContentsMargins(layoutMargin)
        self.lLayout.setContentsMargins(layoutMargin)
        self.gLayout.setContentsMargins(layoutMargin)
        self.arLayout.setContentsMargins(layoutMargin)
        self.odLayout.setContentsMargins(layoutMargin)
        self.csLayout.setContentsMargins(layoutMargin)
        self.hpLayout.setContentsMargins(layoutMargin)
        self.bpmLayout.setContentsMargins(layoutMargin)
        self.starLayout.setContentsMargins(layoutMargin)
        self.lengthLayout.setContentsMargins(layoutMargin)
        self.rankedLayout.setContentsMargins(layoutMargin)
        self.createdLayout.setContentsMargins(layoutMargin)

        labelFixedWidth = 120
        self.qLabel.setFixedWidth(labelFixedWidth)
        self.cLabel.setFixedWidth(labelFixedWidth)
        self.mLabel.setFixedWidth(labelFixedWidth)
        self.sLabel.setFixedWidth(labelFixedWidth)
        self.nsfwLabel.setFixedWidth(labelFixedWidth)
        self.eLabel.setFixedWidth(labelFixedWidth)
        self.rLabel.setFixedWidth(labelFixedWidth)
        self.playedLabel.setFixedWidth(labelFixedWidth)
        self.lLabel.setFixedWidth(labelFixedWidth)
        self.gLabel.setFixedWidth(labelFixedWidth)
        self.arLabel.setFixedWidth(labelFixedWidth)
        self.odLabel.setFixedWidth(labelFixedWidth)
        self.csLabel.setFixedWidth(labelFixedWidth)
        self.hpLabel.setFixedWidth(labelFixedWidth)
        self.bpmLabel.setFixedWidth(labelFixedWidth)
        self.starLabel.setFixedWidth(labelFixedWidth)
        self.lengthLabel.setFixedWidth(labelFixedWidth)
        self.rankedLabel.setFixedWidth(labelFixedWidth)
        self.createdLabel.setFixedWidth(labelFixedWidth)

        enabledCheckboxFixedWidth = 20
        self.cEnabled.setFixedWidth(enabledCheckboxFixedWidth)
        self.mEnabled.setFixedWidth(enabledCheckboxFixedWidth)
        self.sEnabled.setFixedWidth(enabledCheckboxFixedWidth)
        self.nsfwEnabled.setFixedWidth(enabledCheckboxFixedWidth)
        self.eEnabled.setFixedWidth(enabledCheckboxFixedWidth)
        self.rEnabled.setFixedWidth(enabledCheckboxFixedWidth)
        self.playedEnabled.setFixedWidth(enabledCheckboxFixedWidth)
        self.lEnabled.setFixedWidth(enabledCheckboxFixedWidth)
        self.gEnabled.setFixedWidth(enabledCheckboxFixedWidth)
        self.arEnabled.setFixedWidth(enabledCheckboxFixedWidth)
        self.odEnabled.setFixedWidth(enabledCheckboxFixedWidth)
        self.csEnabled.setFixedWidth(enabledCheckboxFixedWidth)
        self.hpEnabled.setFixedWidth(enabledCheckboxFixedWidth)
        self.bpmEnabled.setFixedWidth(enabledCheckboxFixedWidth)
        self.starEnabled.setFixedWidth(enabledCheckboxFixedWidth)
        self.lengthEnabled.setFixedWidth(enabledCheckboxFixedWidth)
        self.rankedEnabled.setFixedWidth(enabledCheckboxFixedWidth)
        self.createdEnabled.setFixedWidth(enabledCheckboxFixedWidth)

        self.qLayout.addWidget(self.qLabel)
        self.qLayout.addWidget(self.qLineEdit)
        self.cLayout.addWidget(self.cEnabled)
        self.cLayout.addWidget(self.cLabel)
        self.cLayout.addWidget(self.cCheckboxWidget)
        self.mLayout.addWidget(self.mEnabled)
        self.mLayout.addWidget(self.mLabel)
        self.mLayout.addWidget(self.mRadioWidget)
        self.sLayout.addWidget(self.sEnabled)
        self.sLayout.addWidget(self.sLabel)
        self.sLayout.addWidget(self.sRadioWidget)
        self.nsfwLayout.addWidget(self.nsfwEnabled)
        self.nsfwLayout.addWidget(self.nsfwLabel)
        self.nsfwLayout.addWidget(self.nsfwRadioWidget)
        self.eLayout.addWidget(self.eEnabled)
        self.eLayout.addWidget(self.eLabel)
        self.eLayout.addWidget(self.eCheckboxWidget)
        self.rLayout.addWidget(self.rEnabled)
        self.rLayout.addWidget(self.rLabel)
        self.rLayout.addWidget(self.rCheckboxWidget)
        self.playedLayout.addWidget(self.playedEnabled)
        self.playedLayout.addWidget(self.playedLabel)
        self.playedLayout.addWidget(self.playedRadioWidget)
        self.lLayout.addWidget(self.lEnabled)
        self.lLayout.addWidget(self.lLabel)
        self.lLayout.addWidget(self.lRadioWidget)
        self.gLayout.addWidget(self.gEnabled)
        self.gLayout.addWidget(self.gLabel)
        self.gLayout.addWidget(self.gRadioWidget)
        self.arLayout.addWidget(self.arEnabled)
        self.arLayout.addWidget(self.arLabel)
        self.arLayout.addWidget(self.arRangeWidget)
        self.odLayout.addWidget(self.odEnabled)
        self.odLayout.addWidget(self.odLabel)
        self.odLayout.addWidget(self.odRangeWidget)
        self.csLayout.addWidget(self.csEnabled)
        self.csLayout.addWidget(self.csLabel)
        self.csLayout.addWidget(self.csRangeWidget)
        self.hpLayout.addWidget(self.hpEnabled)
        self.hpLayout.addWidget(self.hpLabel)
        self.hpLayout.addWidget(self.hpRangeWidget)
        self.bpmLayout.addWidget(self.bpmEnabled)
        self.bpmLayout.addWidget(self.bpmLabel)
        self.bpmLayout.addWidget(self.bpmRangeWidget)
        self.starLayout.addWidget(self.starEnabled)
        self.starLayout.addWidget(self.starLabel)
        self.starLayout.addWidget(self.starRangeWidget)
        self.lengthLayout.addWidget(self.lengthEnabled)
        self.lengthLayout.addWidget(self.lengthLabel)
        self.lengthLayout.addWidget(self.lengthRangeWidget)
        self.rankedLayout.addWidget(self.rankedEnabled)
        self.rankedLayout.addWidget(self.rankedLabel)
        self.rankedLayout.addWidget(self.rankedRangeWidget)
        self.createdLayout.addWidget(self.createdEnabled)
        self.createdLayout.addWidget(self.createdLabel)
        self.createdLayout.addWidget(self.createdRangeWidget)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addLayout(self.qLayout)
        self.vBoxLayout.addLayout(self.cLayout)
        self.vBoxLayout.addLayout(self.mLayout)
        self.vBoxLayout.addLayout(self.sLayout)
        self.vBoxLayout.addLayout(self.nsfwLayout)
        self.vBoxLayout.addLayout(self.eLayout)
        self.vBoxLayout.addLayout(self.rLayout)
        self.vBoxLayout.addLayout(self.playedLayout)
        self.vBoxLayout.addLayout(self.lLayout)
        self.vBoxLayout.addSpacing(7)
        self.vBoxLayout.addLayout(self.gLayout)
        self.vBoxLayout.addLayout(self.arLayout)
        self.vBoxLayout.addLayout(self.odLayout)
        self.vBoxLayout.addLayout(self.csLayout)
        self.vBoxLayout.addLayout(self.hpLayout)
        self.vBoxLayout.addLayout(self.bpmLayout)
        self.vBoxLayout.addLayout(self.starLayout)
        self.vBoxLayout.addLayout(self.lengthLayout)
        self.vBoxLayout.addLayout(self.rankedLayout)
        self.vBoxLayout.addLayout(self.createdLayout)

    def eventFilter(self, watched: PySide6.QtCore.QObject, event: PySide6.QtCore.QEvent) -> bool:
        ...

    def getParams(self):
        """
        get all parameters from widgets
        """
        print(self.rankedRangeWidget.getRange())


# TODO: 限制NumRangeUnit和DateRangeUnit最大框的值必须大于最小框的值
class NumRangeUnit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.minLineEdit = DoubleSpinBox(self)
        self.minLineEdit.setMinimum(0)
        self.sepLabel = QLabel("-", self)
        self.maxLineEdit = DoubleSpinBox(self)
        self.maxLineEdit.setMinimum(0)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.minLineEdit)
        self.hBoxLayout.addWidget(self.sepLabel, alignment=Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.maxLineEdit)
        self.hBoxLayout.addStretch(1)

    def getRange(self):
        return self.minLineEdit.value(), self.maxLineEdit.value()


class DateRangeUnit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.minDateEdit = ZhDatePicker(self) if config["view"]["i18nLanguage"] == "zh_CN" else DatePicker(self)
        self.sepLabel = QLabel("-", self)
        self.maxDateEdit = ZhDatePicker(self) if config["view"]["i18nLanguage"] == "zh_CN" else DatePicker(self)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.minDateEdit)
        self.hBoxLayout.addWidget(self.sepLabel, alignment=Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.maxDateEdit)
        self.hBoxLayout.addStretch(1)

    def getRange(self):
        """ return ((2023, 5, 29), (2023, 7, 29)) """
        return self.minDateEdit.date.getDate(), self.maxDateEdit.date.getDate()


class HRadioWidget(QWidget):
    currentIndexChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.buttons = []  # type: List[RadioButton]
        self.activated = -1

        self.widgetLayout = FlowLayout(self)
        self.widgetLayout.setContentsMargins(0, 13, 0, 15)
        self.widgetLayout.setVerticalSpacing(5)
        self.widgetLayout.setHorizontalSpacing(10)

        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.buttonClicked.connect(self._onItemClicked)

        # self.addAction(QAction(None, None, triggered=))

    def addItem(self, text: str):
        radioButton = RadioButton(text, self)
        # radioButton.clicked.connect(self._onItemClicked(len(self.buttons)))
        self.widgetLayout.addWidget(radioButton)
        self.buttonGroup.addButton(radioButton)
        self.buttons.append(radioButton)

    def addItems(self, texts: List[str]):
        for t in texts:
            self.addItem(t)

    def getActivatedButtonIndex(self):
        return self.activated

    def getActivatedButtonText(self):
        if not 0 <= self.activated < len(self.buttons):
            return ''
        return self.buttons[self.activated].text()

    def setActivatedButton(self, index: int):
        self.buttons[index].click()
        self.activated = index

    def findText(self, text: str):
        for i, item in enumerate(self.buttons):
            if item.text() == text:
                return i

        return -1

    def _onItemClicked(self, button: RadioButton):
        index = self.findText(button.text())
        if index == self.activated:
            return

        print("index: ", index)

        self.activated = index
        self.currentIndexChanged.emit(index)

    # def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None:
    #     painter = QPainter(self)
    #     pen = QPen(QColor("#e5e5e5"), 2, Qt.SolidLine)
    #     if isDarkTheme():
    #         pen.setColor("#2d2d2d")
    #     else:
    #         pen.setColor("#e5e5e5")
    #     painter.setPen(pen)
    #     painter.drawRoundedRect(QRect(0, 0, self.width() - 2, self.height() - 2), 10, 10)


class HCheckboxWidget(QWidget):
    selectedIndexesChanged = Signal(List[int])

    CheckBoxStatusChecked = Qt.CheckState.Checked
    CheckBoxStatusUnchecked = Qt.CheckState.Unchecked

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.checkboxes = []  # type: List[CheckBox]
        self.selections = []
        self.widgetLayout = FlowLayout(self)
        self.widgetLayout.setContentsMargins(0, 13, 0, 15)
        self.widgetLayout.setVerticalSpacing(5)
        self.widgetLayout.setHorizontalSpacing(10)

    def addItem(self, text: str):
        checkbox = CheckBox(text, self)
        self.widgetLayout.addWidget(checkbox)
        self.checkboxes.append(checkbox)
        checkbox.stateChanged.connect(lambda state: self._stateChanged(state, checkbox))

    def addItems(self, texts: List[str]):
        for t in texts:
            self.addItem(t)

    def getSelectedButtonIndexes(self):
        return self.selections

    def getSelectedButtonTexts(self):
        return [checkbox.text() for checkbox in self.checkboxes]

    def _stateChanged(self, state: int, widget: CheckBox):
        index = self.findText(widget.text())
        if index == -1:
            logger.error(f"widget [{widget.text()}]not found")
            return

        if state == 2:
            if index in self.selections:
                return
            self.selections.append(index)
        elif state == 0:
            if index not in self.selections:
                return
            self.selections.remove(index)

    def findText(self, text: str):
        for i, item in enumerate(self.checkboxes):
            if item.text() == text:
                return i

        return -1
