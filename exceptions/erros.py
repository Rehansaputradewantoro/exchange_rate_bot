"""Kelas penanganan kesalahan khusus."""


class APIException(Exception):
    """Kesalahan di tempat kerja API."""

    ...


class ServiceException(Exception):
    """Kesalahan dalam pengoperasian layanan nilai tukar."""

    ...
