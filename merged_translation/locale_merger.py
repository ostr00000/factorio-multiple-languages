import os
from configparser import RawConfigParser
from pathlib import Path
from typing import Tuple, Iterable

from merged_translation.ignore_section_config_parser import IgnoreSectionConfigParser
from merged_translation.zip_function import dictZip


class LocaleMerger:
    SEPARATOR = ' | '

    def __init__(self, gamePath, outLocaleName: str, localeToMerge: Tuple[str, ...],
                 mergerOutput=Path('.').absolute() / 'output'):
        self.gamePath = Path(gamePath)
        self.outLocaleName = outLocaleName
        self.localeToMerge = localeToMerge
        self.myOutput = mergerOutput

    def mergeLocales(self):
        for localeDir in self._findLocale():
            relativePath = localeDir.relative_to(self.gamePath)
            self._mergeLocalesInPath(relativePath)

    def _findLocale(self):
        for localePath in self.gamePath.glob('**/locale'):
            yield localePath

    def _mergeLocalesInPath(self, relativePath: Path):
        localeNameToFiles = {}

        for localeName in self.localeToMerge:
            localeFile = self.gamePath / relativePath / localeName
            localeNameToFiles[localeName] = {f.name: f for f in localeFile.glob('*.cfg')}

        outputPath = self.myOutput / relativePath / self.outLocaleName
        outputPath.mkdir(exist_ok=True, parents=True)

        for fileName, filesToMerge in dictZip(*localeNameToFiles.values()):
            self._mergerTranslations(filesToMerge, outputPath=outputPath / fileName)

    def _mergerTranslations(self, mergeFileNames: Iterable[os.PathLike], outputPath: os.PathLike):
        configs = []
        for mergeFileName in mergeFileNames:
            config = IgnoreSectionConfigParser()
            config.read(mergeFileName)
            configs.append(config)

        outputConfig = IgnoreSectionConfigParser()

        for sectionName, sections in dictZip(*configs):
            newSection = {}
            for trKey, trValues in dictZip(*sections):
                newSection[trKey] = self.SEPARATOR.join(trValues)

            if newSection:
                outputConfig[sectionName] = newSection

        with open(outputPath, 'w') as outputFile:
            outputConfig.write(outputFile, space_around_delimiters=False)
