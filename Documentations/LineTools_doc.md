### Summary of the Flash Programming Tool (FPT)

The Flash Programming Tool (FPT) is used to program a complete SPI image into SPI flash devices. It can program each region individually or all regions with a single command. FPT also allows users to perform various functions such as viewing flash contents, writing flash contents to a log file, performing binary file comparisons, writing to specific address blocks, programming named variables, provisioning HDCP, providing FPF’s access, and assisting with Closemnf.

### System Requirements

- The platform must be bootable with a working BIOS and an operating system.
- FPT must be run on the system with the flash memory to be programmed.
- For Linux, the kernel must have a patch that exposes dedicated sysfs files for FPT to retrieve necessary information.
- The `intel-spi` kernel module argument `writeable` must be set to 1.

### Workflow Example

1. Plug a pre-programmed flash with a bootable BIOS image into a new computer.
2. Boot the computer.
3. Run FPT to write a new BIOS/Intel® ME/GbE image to flash.
4. Power down the computer.
5. Power up the computer to access Intel® ME/GbE capabilities and new custom BIOS features.

### Required Files

- **Windows**: `fptw.exe` and associated files in the same directory.
- **EFI**: `fpt.efi` and associated files in the root directory of the disk.

### Commands and Usage

#### General Commands

- **Help (-H, -?)**: Displays the list of command line options supported by FPT.
- **-VER**: Shows the version of the tools.
- **-EXP**: Shows examples of how to use the tools.
- **-VERBOSE []**: Displays the tool's debug information or stores it in a log file.
- **-NORESET**: Delays the reset and allows users to bundle the resets into one.
- **-Y**: Bypasses prompt, automatically answering with "y".
- **-I**: Displays information about the image currently used in the flash.

#### Flash Operations

- **-F [NOVERIFY]**: Programs a binary file into an SPI flash. The `NOVERIFY` sub-option skips verification.
- **-VERIFY**: Compares a binary to the SPI flash.
- **-NOVERIFY**: Suboption of `-F`, skips verification.
- **-D**: Reads the SPI flash and dumps the flash contents to a file or screen.
- **-DESC**: Read/Write Descriptor region.
- **-BIOS**: Read/Write BIOS region.
- **-ME**: Read/Write Intel® ME region.
- **-GBE**: Read/Write GbE region.
- **-PDR**: Read/Write PDR region.
- **-EC**: Read/Write EC region.
- **-SAVEMAC**: Saves the GbE MAC Address.
- **-SAVESXID**: Saves the GbE SSID and SVID.
- **-E**: Skips the erase operation before writing.
- **-REWRITE**: Rewrites the SPI with file data even if flash is identical.
- **-A, -ADDRESS**: Specifies the start address for read, verify, or write operations.
- **-L, -LENGTH**: Specifies the length of data to be read, written, or verified.

#### NVAR and FPF Operations

- **-CVARS**: Lists all the current manufacturing line configurable variables.
- **-MASTERACCESSGEN**: Generates a Manufacturing Line Configurable Master Access Input File.
- **-CFGGEN**: Creates a file to update line configurable NVARs.
- **-U**: Updates the NVARs and FPFs in the flash.
- **-CLEAR**: Overwrites a pending NVAR value update request with the file system's current.
- **-O**: Specifies the output file for NVAR information.
- **-IN**: Specifies the input file for NVAR input.
- **-N**: Specifies the name of the NVAR to update.
- **-V**: Specifies the value for the NVAR variable.
- **-CLOSEMNF**: Executes end of manufacturing phase operations.
- **-GRESET**: Performs a global reset.
- **-PAGE**: Pauses the screen when a page of text has been reached.
- **-R**: Retrieves NVAR value for a specific NVAR file name.
- **-VARS**: Displays all variables supported for the `-R` and `-COMPARE` commands.
- **-COMMIT**: Commits all setfile commands NVARs changes to NVAR and causes relevant reset accordingly.
- **-DISABLEME**: Disables the Management Engine.
- **-FPFS**: Displays a list of the FPFs.
- **-GETPID**: Retrieves the part ID.
- **-WRITETOKEN**: Writes the token where the file name is the token name.
- **-ERASETOKEN**: Deletes the token.
- **-COMMITFVCSVN**: Sends the minimum supported Anti Rollback Security Version (SVN).
- **-STRAPUPDATE**: Updates Manufacturing Line Configurable SoftStrap.
- **-READSTRAPS**: Reads all the softStraps.
- **-StartPSR**: Initiates PSR logging into the Intel® CSME FW.
- **-EnableUpid**: Enables UPID State.
- **-DisableUpid**: Disables UPID State.
- **-getUPIDcertChain**: Retrieves and stores the UPID certificate chain to a file.

### Examples

#### Complete SPI Flash Device with Binary File

```sh
fpt.exe –f spi.bin
fpt.efi –f spi.bin
```

#### Program Specific Region

```sh
fpt.exe –f bios.rom –BIOS
fpt.efi –f bios.rom –BIOS
```

#### Program SPI Flash from Specific Address

```sh
fpt.exe -F image.bin -A 0x100 -L 0x800
fpt.efi -F image.bin -A 0x100 -L 0x800
```

#### Dump Full Image

```sh
fpt.exe –d imagedump.bin
fpt.efi –d imagedump.bin
```

#### Dump Specific Region

```sh
fpt.exe –d descdump.bin –desc
fpt.efi –d descdump.bin –desc
```

#### Display SPI Information

```sh
fptw.exe –I
```

#### Verify Image with Errors

```sh
fpt.exe -verify outimage.bin
fpt.efi -verify outimage.bin
```

#### Verify Image Successfully

```sh
fpt.exe -verify outimage.bin
fpt.efi -verify outimage.bin
```

#### Get Intel® ME settings

```sh
fpt.exe –r “Privacy/SecurityLevel”
fpt.efi –r “^”Privacy/SecurityLevel”^”
```

#### CVAR Configuration File Generation

```sh
fpt.exe –cfggen [-o ] [options]
```

This summary provides an overview of the FPT tool, its usage, and the commands available for various operations.


### Summary of Intel® ME Manuf and ME ManufWin Tool

**Purpose:**
Intel® ME Manuf and ME ManufWin are tools designed to validate the functionality of Intel® Management Engine (ME) on the manufacturing line. These tools ensure that all Intel® ME components on the test board have been correctly assembled and are functioning as expected. They do not check for LAN functionality but validate other components and flows according to the firmware (FW) installed on the platform.

**Key Features:**
- Validates Intel® ME applications such as BIOS-FW, Flash, SMBus, KVM, etc.
- Requires administrator privileges to run on Windows® OS.
- Can be used in Windows® PE environment with manual driver loading.
- Capable of running Built-In Self Tests (BIST) and End-Of-Line (EOL) checks.
- Reports test results or failure messages and may trigger reboots for further testing.

### How to Use the Tool

1. **Running the Tool:**
   - Ensure you have administrator privileges.
   - Open the Command Line Interface (CLI) using the "Run as Administrator" option in Windows® 10.
   - Execute the tool using the command `MEManufWin64.exe` followed by the desired options.

2. **Windows® PE Environment:**
   - Manually load the driver with the .inf file from the Intel® MEI driver installation files.
   - Use the command `drvload HECI.inf` to load the driver into the running system each time Windows® PE reboots. 

3. **Running Tests:**
   - The tool checks the FW SKU and runs the appropriate tests unless specified otherwise.
   - If Intel® AMT is enabled, the system may reboot to test hardware connections in sleep state.
   - The tool can remember previous test results and will either run the test or report the result.

4. **End-Of-Line (EOL) Checks:**
   - Use the `-EOL` option to run checks ensuring all settings and configurations meet Intel requirements before shipping.
   - Modify the `MEManuf.xml` configuration file to select specific tests and expected values.

### Tool Commands and Their Usage

| Option         | Description                                                                                    
 |
|----------------|-------------------------------------------------------------------------------------------------|
| No option      | Runs tests based on the firmware SKU type.                                                     
 |
| -EXP           | Shows examples of how to use the tools.                                                        
 |
| -H or -?       | Displays the help screen.                                                                      
 |
| -VER           | Shows the version of the tools.                                                                
 |
| -S0            | Runs runtime BIST test without power reset/hibernation.                                        
 |
| -NEXTREBOOT    | Performs CM3 Autotest on the next platform reboot.                                             
 |
| -TEST          | Runs a full BIST test.                                                                         
 |
| -BISTRESULT    | Returns the last BIST results.                                                                 
 |
| -EOL           | Runs EOL checks to ensure all settings and configurations are correct before shipping.         
 |
| -CFGGEN        | Generates a default configuration file for EOL checks.                                         
 |
| -F <filename>  | Loads a customer-defined configuration file.                                                   
 |
| -VERBOSE       | Displays debug information or stores it in a log file.                                         
 |
| -PAGE          | Pauses the display when information exceeds one screen.                                        
 |
| -ALL           | Generates all possible tests for the configuration file.                                       
 |
| -LEVEL         | Selects EOL tests level (between 1 & 3).                                                       
 |

### Example Commands

1. **Running the Tool with No Options:**
   ```sh
   MEManufWin64.exe
   ```

2. **Displaying Help Screen:**
   ```sh
   MEManufWin64.exe -H
   ```

3. **Running a Full BIST Test:**
   ```sh
   MEManufWin64.exe -TEST
   ```

4. **Running EOL Checks:**
   ```sh
   MEManufWin64.exe -EOL
   ```

5. **Generating a Default Configuration File:**
   ```sh
   MEManufWin64.exe -CFGGEN myconfig.xml
   ```

6. **Loading a Custom Configuration File:**
   ```sh
   MEManufWin64.exe -F customconfig.cfg
   ```

### Example Output

**Consumer Intel® ME FW SKU:**
```sh
Intel (R) ME Manuf Version: 18.x.x.xxxx
...
MEManuf Operation Passed
```

**Corporate Intel® ME FW SKU:**
```sh
Intel (R) ME Manuf Version: 18.x.x.xxxx
...
MEManuf Operation Passed
```

This summary provides an overview of the Intel® ME Manuf and ME ManufWin tools, their usage, and the available commands to perform various tests and checks on Intel® ME-enabled platforms.

### Summary of Intel® ME Info Tool

**Purpose:**
Intel® ME Info (MEInfoWin and MEInfoWin64.exe) is a diagnostic tool used to check the status and retrieve information about the Intel® Management Engine (ME) firmware (FW). It verifies if the Intel® ME FW is operational and provides detailed information about the firmware, including Intel® Active Management Technology (AMT) and other manageability features.

**Usage:**
- **Windows OS:** Requires administrator privileges. Use the "Run as Administrator" option to open the CLI in Windows® 10.
- **Windows PE Environment:** Manually load the Intel® MEI driver using the .inf file with the command `drvload HECI.inf` each time Windows® PE reboots.
- **Chrome OS:** Enable Developer Mode, switch to terminal 2, verify MEI driver, plug in USB with MEInfo tool, and run the tool from the USB drive.

**Manageability Configurations:**
- Disabling Manageability HW through specific settings will affect the output of Intel® ME Info, showing the image type as consumer and disabling network interfaces.

### Command Line Options and Usage

**Command Syntax:**
```
MEInfoWin64.exe [options]
```

**Options:**
- **-VALUE <value>:** Compares the value of the given feature name (and optional column name) with the value in the command line. Example: `-feat "PTT FPF"`.
- **-FITVER:** Displays MFIT version information.
- **-FEAT <name> <column>:** Retrieves the current value for the specified feature (and optional column name). Example: `-feat "PTT FPF"`.
- **-FWSTS:** Decodes the Intel® ME FW status register value field for easy readability.
- **-VERBOSE <filename>:** Turns on additional information for debugging purposes. Must be used with other options.
- **-H or -?:** Displays the list of command line options supported by the tool.
- **-VER:** Shows the version of the tools.
- **-PAGE:** Pauses the display when it takes more than one screen to show all the information.
- **-EXP:** Shows examples of how to use the tools.
- **No option:** Reports information for all components listed in the documentation for full SKU FW.

### Example Commands

1. **Check Setup and Configuration Process:**
   ```
   MEINFO.exe -feat "Setup and Configuration" –value "Not Completed"
   ```
   Output:
   ```
   Intel(R) ME INFO Version: 18.x.x.xxxx
   Copyright(C) 2005 - 2017, Intel Corporation. All rights reserved.
   Local FWUpdate: Success - Value matches FW value.
   ```

2. **EFI Shell Version:**
   ```
   MEINFO.efi -feat “^"Setup and Configuration"^” –value “^"Not Completed"^”
   ```
   Output:
   ```
   Intel(R) ME INFO Version: 18.x.x.xxxx
   Copyright(C) 2005 - 2017, Intel Corporation. All rights reserved.
   Local FWUpdate: Success - Value matches FW value.
   ```

### List of Components Displayed by Intel® ME Info

The tool retrieves and displays various components and their statuses, including but not limited to:
- Tools Version
- General FW Information
- FW Image Type
- Last ME Reset Reason
- BIOS Boot State
- Current Boot Partition
- Intel® ME Code Versions
- IUPs Information
- PCH Information
- Flash Information
- FW Capabilities
- Intel® Active Management Technology
- Intel® Protected Audio Video Path
- Security Version Numbers
- FW Supported FPFs

### Detailed Information Displayed

The tool provides detailed information about the firmware, including:
- FW Status Registers
- General FW Information (e.g., Current FW State, FW Initialization Complete)
- Intel® ME Code Versions (e.g., BIOS Version, MEI Driver Version, FW Version)
- IUPs Information (e.g., PMC FW Version, ISHC FW Version)
- PCH Information (e.g., PCH Name, PCH Device ID)
- Flash Information (e.g., Storage Device Type, SPI Flash ID)
- Master Access Permissions (e.g., BIOS Read/Write Access)
- End Of Manufacturing (e.g., EOM Settings, NVAR Configuration State)
- Security Version Numbers (e.g., Trusted Computing Base SVN)
- Debug Information (e.g., Token Present, DFx Policy)
- HW Glitch Detection (e.g., TRC State, TRC Fuse)
- Intel® Platform Trust Technology (e.g., Intel® PTT Initial Power-up State)

### Conclusion

Intel® ME Info is a comprehensive tool for diagnosing and retrieving detailed information about the Intel® ME firmware. It is essential for system administrators and IT professionals to ensure the proper functioning and configuration of Intel® ME and related manageability features.