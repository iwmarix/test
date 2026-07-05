#!/usr/bin/env python3
"""Ekstrakcja tekstu ze starych binarnych plików Word (.doc, format OLE2).

Czyta tablicę fragmentów (piece table) z FIB, dzięki czemu poprawnie
odczytuje teksty UTF-16 (polskie znaki) tam, gdzie LibreOffice/antiword
zawodzą.

Użycie:
    pip install olefile
    python3 extract_doc.py wejscie.doc wyjscie.txt

Dla plików .docx użyj:  python3 -c "..." albo pandoc/LibreOffice —
ten skrypt obsługuje wyłącznie stary format binarny.
"""
import struct
import sys

import olefile


def extract(path):
    ole = olefile.OleFileIO(path)
    word = ole.openstream('WordDocument').read()
    which_tbl = (struct.unpack('<H', word[0x000A:0x000C])[0] >> 9) & 1
    table = ole.openstream('1Table' if which_tbl else '0Table').read()
    fc_clx, lcb_clx = struct.unpack('<II', word[0x01A2:0x01AA])
    clx = table[fc_clx:fc_clx + lcb_clx]

    pos = 0
    plcpcd = None
    while pos < len(clx):
        tag = clx[pos]
        if tag == 2:  # Pcdt
            lcb = struct.unpack('<I', clx[pos + 1:pos + 5])[0]
            plcpcd = clx[pos + 5:pos + 5 + lcb]
            break
        elif tag == 1:  # Prc — pomiń
            cb = struct.unpack('<H', clx[pos + 1:pos + 3])[0]
            pos += 3 + cb
        else:
            raise ValueError('nieznany bajt CLX %r na pozycji %d' % (tag, pos))
    if plcpcd is None:
        raise ValueError('brak Pcdt w CLX')

    n = (len(plcpcd) - 4) // 12
    cps = struct.unpack('<%dI' % (n + 1), plcpcd[:4 * (n + 1)])
    out = []
    off = 4 * (n + 1)
    for i in range(n):
        pcd = plcpcd[off + i * 8: off + (i + 1) * 8]
        fc = struct.unpack('<I', pcd[2:6])[0]
        compressed = (fc >> 30) & 1
        fc_val = fc & 0x3FFFFFFF
        cch = cps[i + 1] - cps[i]
        if compressed:
            start = fc_val // 2
            out.append(word[start:start + cch].decode('cp1252', errors='replace'))
        else:
            out.append(word[fc_val:fc_val + 2 * cch].decode('utf-16-le', errors='replace'))
    return ''.join(out)


def main():
    if len(sys.argv) != 3:
        sys.exit('użycie: extract_doc.py wejscie.doc wyjscie.txt')
    text = extract(sys.argv[1])
    text = text.replace('\r', '\n').replace('\x07', '\n').replace('\x0b', '\n')
    text = ''.join(c for c in text if c in '\n\t' or ord(c) >= 32)
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        f.write(text)
    print('%d znaków zapisano do %s' % (len(text), sys.argv[2]))


if __name__ == '__main__':
    main()
