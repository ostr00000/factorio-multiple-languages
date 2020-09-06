def main():
    import logging

    from merged_translation.locale_merger import LocaleMerger

    logging.basicConfig()

    lm = LocaleMerger(
        gamePath='~/factorio',
        outLocaleName='it-pl-en',
        localeToMerge=('it', 'pl', 'en'),
    )
    lm.mergeLocales()


if __name__ == '__main__':
    main()
