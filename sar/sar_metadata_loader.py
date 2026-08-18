from .sar_metadata import AcquisitionMetadata


def create_acquisition_metadata(
    *,
    platform: str,
    sensor: str,
    acquisition_date: str,
    polarization: str,
    orbit_direction: str,
    relative_orbit: int,
    beam_mode: str,
    frequency_band: str,
    incidence_angle: float | None = None,
) -> AcquisitionMetadata:
    """
    Create an AcquisitionMetadata object.
    """

    return AcquisitionMetadata(
        platform=platform,
        sensor=sensor,
        acquisition_date=acquisition_date,
        polarization=polarization,
        orbit_direction=orbit_direction,
        relative_orbit=relative_orbit,
        beam_mode=beam_mode,
        frequency_band=frequency_band,
        incidence_angle=incidence_angle,
    )
