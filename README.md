# SiPM_DS_Analysis
Analysis code for SiPM tile tests and characterization for DarkSide

## Instructions for running on data

### Plotting raw waveforms
Use SiPM_plot.py to plot the raw waveforms to see where the trigger peak is, and to check the noise levels. This is run with 

        python SiPM_plot.py
        
and it will output six pdf files of the first six raw waveforms. 

### Analyzing the waveforms
read_txt.py and analyze_data.py are designed to analyse data from a SiPM tile, saved as a txt file with the amplitudes. The text file is expected to have headers with the record length, board ID, event number, pattern, trigger time stamp, and DC offset. The trigger time stamp is used to calculate the DCR (time difference between SiPM responses) and the record length is used to split into individual waveforms.

To run:

    python read_txt.py wave4
    python analyze_data.py wave4.pickle

read_txt.py will output a pickle file, that is then read into analyze_data.py to form a energy spectrum, with and without a convolution calculation.

read_txt.py calculates the average noise (start of the waveform), and uses a scanned integration window to calculate the max of the waveform for use in the energy calculation. By defining energy values around single photoelectron peaks, average waveforms for single, two, three, etc. photoelectrons are calculated. The single photoelectron peak is used as a template waveform for the convolution algorithm, with the output waveform saved in the pickle file. It also saves the timestamps of each waveform, which is used to calculate the DCR.

In read_txt.py, if energy values for the photo-electron peaks are known, these can be used to choose waveforms with 1, 2, and 3 PEs to make average waveforms. These values can be edited. Additionally, need to edit if there are events with a high trigger rate (at the beginning of a run) that need to be cut out, and edit the energy cut for the DCR calculation (the point between the pedistal and first photo-electron peak). 
