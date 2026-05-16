import zipfile
import os
import calendar
from dataclasses import dataclass
import zlib
import ctypes
import struct
from typing import BinaryIO

oodle = ctypes.cdll.LoadLibrary("./oo2core_8_win64.dll")


@dataclass
class ExportedFileInfo:
    filename: str
    CRC: int
    datetime: int
    compressType: int
    decompressedBytes: bytes | None = None


def fetchPaksList(gameRootPath):
    pakList = []
    fpath = os.path.join(gameRootPath, "PaksList.lst")
    with open(fpath, "r") as f:
        pakList = [os.path.join(gameRootPath, line.strip()) for line in f]
    return pakList


def unPak(pakFilePath, exportRootPath):
    with zipfile.ZipFile(pakFilePath) as zf:
        zipFileInfos = zf.infolist()
        for zipFileInfo in zipFileInfos:
            ret = ExportedFileInfo(
                filename=zipFileInfo.filename,
                CRC=zipFileInfo.CRC,
                datetime=calendar.timegm(zipFileInfo.date_time),
                compressType=zipFileInfo.compress_type,
                decompressedBytes=None,
            )
            if zipFileInfo.compress_type == 15:
                with open(pakFilePath, "rb") as f:
                    ret.decompressedBytes = decompress_oodle(f, zipFileInfo)
            else:
                ret.decompressedBytes = zf.read(zipFileInfo)
            if ret.decompressedBytes == None:
                raise Exception(
                    f"Blank decompressedData: {pakFilePath} at {hex(zipFileInfo.header_offset)}"
                )
            dumpFile(ret, exportRootPath)


def decompress_oodle(f: BinaryIO, zipFileInfo: zipfile.ZipInfo):
    f.seek(zipFileInfo.header_offset + 26, 0)
    fileNameLen, extraFieldLen = struct.unpack("HH", f.read(4))
    f.seek(fileNameLen + extraFieldLen, 1)

    compressed = f.read(zipFileInfo.compress_size)
    dst = ctypes.create_string_buffer(zipFileInfo.file_size)
    oodle.OodleLZ_Decompress(
        compressed,
        zipFileInfo.compress_size,
        dst,
        zipFileInfo.file_size,
        0,
        0,
        0,
        None,
        None,
        None,
        None,
        None,
        None,
        3,
    )
    return dst.raw


def dumpFile(fileInfo: ExportedFileInfo, rootPath: str):
    fpath = os.path.join(rootPath, fileInfo.filename)
    os.makedirs(os.path.dirname(fpath), exist_ok=True)

    if fileInfo.decompressedBytes is None:
        raise ValueError("no data")

    data = fileInfo.decompressedBytes

    with open(fpath, "wb") as f:
        f.write(data)

    os.utime(fpath, (fileInfo.datetime, fileInfo.datetime))

    # Performs CRC checks for files using custom compression methods
    if fileInfo.compressType == 15:
        calc_crc = zlib.crc32(data) & 0xFFFFFFFF
        if calc_crc != fileInfo.CRC:
            raise ValueError(
                f"CRC mismatch: {fileInfo.filename} "
                f"expected={hex(fileInfo.CRC)} got={hex(calc_crc)}"
            )

    print(f"[OK] {fileInfo.filename}")


def main():
    gameRootPath = r"E:\SteamLibrary\steamapps\common\New World"
    exportRootPath = r"E:\output"
    pakList = fetchPaksList(gameRootPath)
    for pakFilePath in pakList:
        print(pakFilePath)
        unPak(pakFilePath, exportRootPath)


main()
