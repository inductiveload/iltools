
import requests
import defusedxml.ElementTree as ET

from . import pagelist
import logging

class IaSource():

    def __init__(self, id):
        self.id = id
        self.meta = None

    def _get_download_url(self, filename):

        url = "https://archive.org/download/{iaid}/{fn}".format(
                    iaid=self.id, fn=filename)
        return url

    def _get_metadata(self):

        # check memoised
        if self.meta is not None:
            return self.meta

        # logging.debug("Getting IA file list for {}".format(self.id))
        url = "https://archive.org/metadata/{iaid}".format(iaid=self.id)

        r = requests.get(url)
        r.raise_for_status()
        self.meta = r.json()

        assert(self.meta is not None)

    def _get_files_with_format(self, fmts):

        self._get_metadata()

        for f in self.meta['files']:
            if f['format'] in fmts:
                return f['name']

        return None

    def _get_scandata_xml(self):

        scandata_name = self._get_files_with_format(["Scandata", "Scribe Scandata ZIP"])

        if scandata_name.endswith(".zip"):
            scandata_name += "/scandata.xml"

        sdurl = self._get_download_url(scandata_name)

        r = requests.get(sdurl)
        r.raise_for_status()
        xml = ET.fromstring(r.content)

        return xml


    def get_pagelist(self):
        logging.debug("Getting IA pagelist for ID {}".format(self.id))

        xml = self._get_scandata_xml()

        pages = xml.findall(".//{*}pageData/{*}page")

        pl = pagelist.PageList()

        for pg in pages:

            addPage = pg.find(".{*}addToAccessFormats")

            if addPage is not None and addPage.text.lower() == "false":
                continue

            pageTypeE = pg.find(".{*}pageType")
            pn = ""
            if pageTypeE is not None:

                if pageTypeE.text in ["Title", "Title Page"]:
                    pn = "Title"
                elif pageTypeE.text in ["Cover"]:
                    pn = "Cover"

            if not pn:

                pageNumberE = pg.find(".{*}pageNumber")

                if pageNumberE is None or pageNumberE.text is None:
                    pn = "–"
                else:
                    pn = pageNumberE.text

            pl.append(pn)

        return pl