# Helsinki O2 Pathway Tool

Helsinki O2 Pathway Tool is a tool for modeling oxygen pathway visually and numerically with non-invasive or invasive measurement data.
The tool combines Fick's law of diffusion and Fick's principle to calculate oxygen diffusion in the muscle. The model estimates
partial pressure of oxygen in venous blood taking also the core temperature and arterial blood's pH into account. The tool was 
designed and developed as a healthtech engineering bachelor's thesis work. The tool was designed and developed in collaboration 
with exercise physiologists in Helsingin Urheilulääkäriasema in Helsinki, Finland.

The Helsinki O2 Pathway Tool uses information about (at least): 
- oxygen consumption (VO2)
- heart rate (HR)
- stroke volume (SV)
- cardiac output (Q)
- hemoglobin concentration ([Hb])
- oxygen saturation of arterial blood (SaO2). 

You can also input information about:
- oxygen content of arterial blood (CaO2)
- oxygen content of venous blood (CvO2)
- difference of oxygen content in arterial-venous blood (CavO2)
- oxygen saturation of venous blood (SvO2)
- partial pressure of oxygen in venous blood (PvO2)
- oxygen convection (QaO2)
- core temperature
- pH

<p>See the more detailed information about the tool and its function in the userInstructions.pdf or inside the tool's Help menu</p>

<h2>How to get started?</h2>

<h3>Windows</h3>
<ul>
<li>1. Download the Helsinki O2 Pathway Tool</li>
    <ul>
        <li>1. Click "Releases" on the right side of this page</li>
        <li>2. Click "Assets"-dropdownmenu on the latest version</li>
        <li>3. Click "HO2PT_Windows.rar"</li>
        <li>4. Download should start automatically</li>
    </ul>
<li>2. Unpack the downloaded file</li>
<li>3. Execute O2PathwayTool.exe</li>
<li>4. Happy modeling!</li>
</ul>

<h3>Linux</h3>
<ul>
<li>1. Download the Helsinki O2 Pathway Tool</li>
    <ul>
        <li>1. Click "Releases" on the right side of this page</li>
        <li>2. Click "Assets"-dropdownmenu on the latest version</li>
        <li>3. Click "HO2PT_Linux.rar"</li>
        <li>4. Download should start automatically</li>
    </ul>
<li>2. Unpack the downloaded file</li>
<li>3. Execute O2PathwayTool.exe</li>
<li>4. Happy modeling!</li>
</ul>

<h3>MacOS</h3>
<p>Due to the inexperience in MacOS of the developers the Helsinki O2 Pathway Tool app does not run as intended. To start the tool you must use the executable file inside the O2PathwayTool.app contents.</p>
<ul>
<li>1. Download the Helsinki O2 Pathway Tool</li>
    <ul>
        <li>1. Click "Releases" on the right side of this page</li>
        <li>2. Click "Assets"-dropdownmenu on the latest version</li>
        <li>3. Click "HO2PT_macOS.rar"</li>
        <li>4. Download should start automatically</li>
    </ul>
<li>2. Unpack the downloaded file</li>
<li>3. Right click on the O2PathwayTool.app</li>
<li>4. Click "Show package contents"</li>
<li>5. Run the O2PathwayTool in "Contents/MacOS"</li>
<li>6. Happy modeling!</li>
</ul>

<h3>What kind of data can I use?</h3>

The tool can read and save excel-files (.xlsx). Your data can be formatted in multiple ways and have multiple sheets, 
that is why O2PathwayTool has an importing tool which guides you through the importing process. 

<h3>How about exporting results?</h3>

The O2PathwayTool makes a copy of your data, so you don't have to worry about overriding your existing data. Results can be 
exported into a new excel file or they can be concatenated to the same file that was used to import data.

<h3>Do I need measurement data?</h3>

No. You can create projects, subjects, tests and input data by hand. 
