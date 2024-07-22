#FITS Calibration and Light Frame Calibration

import os
import numpy as np
from astropy.io import fits

# Define the directory paths for darks, flats, and lights
darks_directory = 'Darks Path'
flats_directory = 'Flat Path''
lights_directory = 'Lights Path'

# Combine the dark frames
dark_frames = []
for file_name in os.listdir(darks_directory):
 if file_name.endswith('.fit'):
        file_path = os.path.join(darks_directory, file_name)
 with fits.open(file_path) as hdul:
            dark_frame = hdul[0].data
            dark_frames.append(dark_frame)

master_dark = np.median(dark_frames, axis=0)

# Save the master dark frame as a FITS file
master_dark_path = os.path.join(darks_directory, 'master_dark.fit')
hdu = fits.PrimaryHDU(master_dark)
hdul = fits.HDUList([hdu])
hdul.writeto(master_dark_path, overwrite=True)

# Combine the flat frames
flat_frames = []
for file_name in os.listdir(flats_directory):
 if file_name.endswith('.fit'):
        file_path = os.path.join(flats_directory, file_name)
 with fits.open(file_path) as hdul:
            flat_frame = hdul[0].data
            flat_frames.append(flat_frame)

master_flat = np.median(flat_frames, axis=0)

# Save the master flat frame as a FITS file
master_flat_path = os.path.join(flats_directory, 'master_flat.fit')
hdu = fits.PrimaryHDU(master_flat)
hdul = fits.HDUList([hdu])
hdul.writeto(master_flat_path, overwrite=True)

# Create a directory to store the calibrated light frames
calibrated_directory = os.path.join(lights_directory, 'calibrated')
os.makedirs(calibrated_directory, exist_ok=True)

# Calibrate the light frames
for file_name in os.listdir(lights_directory):
 if file_name.endswith('.fit'):
        file_path = os.path.join(lights_directory, file_name)
 with fits.open(file_path) as hdul:
            light_frame = hdul[0].data

 # Subtract the master dark from the light frame
 calibrated_frame = light_frame - master_dark

 # Normalize the light frame with the master flat
 calibrated_frame /= master_flat

 # Save the calibrated light frame as a new FITS file
 calibrated_file_path = os.path.join(calibrated_directory, file_name)
            hdu = fits.PrimaryHDU(calibrated_frame)
            hdul = fits.HDUList([hdu])
            hdul.writeto(calibrated_file_path, overwrite=True)
