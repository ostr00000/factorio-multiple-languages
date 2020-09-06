from configparser import RawConfigParser, MissingSectionHeaderError, DEFAULTSECT


class IgnoreSectionConfigParser(RawConfigParser):

    def _read(self, fp, fpname):
        try:
            return super()._read(fp, fpname)
        except MissingSectionHeaderError:
            return super()._read(self._fakeHeaderFile(fp), fpname)

    @staticmethod
    def _fakeHeaderFile(fp):
        yield f'[{DEFAULTSECT}]'
        yield from fp

    def _write_section(self, fp, section_name, section_items, delimiter):
        """Write a single section to the specified `fp'.
        Section default does not have header.
        """
        if section_name != self.default_section:
            fp.write("[{}]\n".format(section_name))

        for key, value in section_items:
            value = self._interpolation.before_write(self, section_name, key,
                                                     value)
            if value is not None or not self._allow_no_value:
                value = delimiter + str(value).replace('\n', '\n\t')
            else:
                value = ""
            fp.write("{}{}\n".format(key, value))
        fp.write("\n")
