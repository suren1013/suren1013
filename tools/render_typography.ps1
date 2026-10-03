# Original raster motion typography. Requires System.Drawing and FFmpeg.
param([string]$FFmpeg = 'C:/Program Files/Shutter Encoder/Library/ffmpeg.exe')
Add-Type -AssemblyName System.Drawing
$repoRoot = Split-Path $PSScriptRoot -Parent
$assetsRoot = Join-Path $repoRoot 'assets'
$framesRoot = Join-Path $repoRoot 'build/typography'
New-Item -ItemType Directory -Path $framesRoot -Force | Out-Null
$ink = [System.Drawing.ColorTranslator]::FromHtml('#111214')
$paper = [System.Drawing.ColorTranslator]::FromHtml('#e5e1d8')
$red = [System.Drawing.ColorTranslator]::FromHtml('#ca5148')
$muted = [System.Drawing.ColorTranslator]::FromHtml('#aeaea7')
function Brush($color) { New-Object System.Drawing.SolidBrush($color) }
function Text($g, $text, $x, $y, $size, $color, $face='Arial', $bold=$false) {
    $style = [System.Drawing.FontStyle]::Regular
    if ($bold) { $style = [System.Drawing.FontStyle]::Bold }
    $font = New-Object System.Drawing.Font($face, $size, $style, ([System.Drawing.GraphicsUnit]::Pixel))
    $brush = Brush $color
    $g.DrawString($text, $font, $brush, [float]$x, [float]$y)
    $font.Dispose(); $brush.Dispose()
}
function Rect($g, $color, $x, $y, $w, $h) {
    $b = Brush $color
    $g.FillRectangle($b, [float]$x, [float]$y, [float]$w, [float]$h)
    $b.Dispose()
}
$panels = @(
    @{name='practice'; h=320; num='01'; tag='MECHANICAL ENGINEERING / COMPUTATION'; title='PHYSICS INTO'; title2='WORKING SYSTEMS.'; footer='MODEL THE PROBLEM.  /  VALIDATE THE RESULT.  /  BUILD SOMETHING USEFUL.'},
    @{name='status'; h=370; num=''; tag='THE PRACTICE / PRESENT TENSE'; title='IN PROGRESS.'; rows=@(@('BUILDING','Engineering tools, simulations, and useful software'),@('FOCUS','Thermal engineering / forced-air cooling / CFD'),@('LEARNING','OpenFOAM, numerical methods, engineering code'),@('DRIVEN BY','Curiosity, clear reasoning, systems that work'))},
    @{name='disciplines'; h=360; num=''; tag='THREE DISCIPLINES / ONE ENGINEERING WORKFLOW'; title='PHYSICAL. DIGITAL.'; columns=@(@('01','MECHANICAL','Heat transfer / thermal systems','Machine design','Engineering problem-solving'),@('02','SIMULATION','CFD / FEA','Numerical modelling','Physical systems into models'),@('03','SOFTWARE','Web tools / automation','AI-assisted workflows','Software for engineering'))},
    @{name='selected-work'; h=200; num='03'; tag='SELECTED WORK / ENGINEERING, ANALYTICS & LIVE SYSTEMS'; title='BUILT TO WORK.'; footer='THREE PROJECTS.  /  THREE REAL PROBLEMS.'},
    @{name='casting'; h=280; num='01'; tag='PROJECT FILE / ENGINEERING SOFTWARE'; title='CASTING ASSISTANT'; metrics=@(@('06','ALLOYS'),@('3D','RISER SCHEMATIC'),@('MODULUS','YIELD / FEEDING / RISK')); footer='TYPESCRIPT  /  REACT  /  REACT THREE FIBER'},
    @{name='clv'; h=280; num='02'; tag='PROJECT FILE / CUSTOMER ANALYTICS'; title='CUSTOMER CLV'; metrics=@(@('10','CLEANING STEPS'),@('12','CUSTOMER METRICS'),@('07','RFM SEGMENTS')); footer='PYTHON  /  STREAMLIT  /  PANDAS  /  PLOTLY'},
    @{name='election'; h=280; num='03'; tag='PROJECT FILE / LIVE SYSTEMS'; title='TN ELECTION LIVE'; metrics=@(@('234','CONSTITUENCIES'),@('60s','DATA REFRESH'),@('LIVE','MAJORITY TRACKING')); footer='TYPESCRIPT  /  REACT  /  GOOGLE CLOUD RUN'},
    @{name='palette'; h=370; num='04'; tag='WORKING PALETTE / ENGINEERING + CODE + TOOLS'; title='TOOLS OF THE TRADE.'; columns=@(@('I','ENGINEERING','OpenFOAM / ANSYS / SolidWorks','CFD / FEA','Heat Transfer'),@('II','CODE','Python / TypeScript / JavaScript','React / Next.js','Java'),@('III','TOOLS','Git / GitHub','VS Code','LangChain'))},
    @{name='principles'; h=430; num='05'; tag='BUILD PRINCIPLES / A WORKING METHOD'; title='REASON. BUILD. REFINE.'; principles=@('Understand the physical system before abstracting it.','Make assumptions visible and results measurable.','Build the smallest useful version, then validate it.','Use AI to accelerate judgment - not replace it.','Close the loop: learn from the result and improve the model.')},
    @{name='workflow'; h=370; num=''; tag='METHOD / FROM PHYSICAL QUESTION TO USEFUL TOOL'; title='CLOSE THE LOOP.'; stages=@(@('01','QUESTION','Define the system','and its constraints.'),@('02','MODEL','State assumptions.','Choose the physics.'),@('03','SIMULATE','Explore behaviour.','Compare alternatives.'),@('04','VALIDATE','Check the result.','Expose uncertainty.'),@('05','BUILD','Make it useful.','Learn and refine.')); footer='PROBLEM  /  MODEL  /  SIMULATE  /  VALIDATE  /  BUILD  /  REPEAT'},
    @{name='research'; h=420; num=''; tag='RESEARCH DIRECTIONS / CURRENT FOCUS + LONG-TERM INTERESTS'; title='THE NEXT HORIZON.'; columns=@(@('01','THERMAL SYSTEMS','Avionics heat sinks','Forced-air cooling','OpenFOAM-based CFD'),@('02','FLUID MECHANICS','Flow behaviour','Numerical methods','Aerospace applications'),@('03','SPACE SYSTEMS','Structures','Thermal management','Rotating space habitats')); footer='CURRENT: THERMAL ENGINEERING & CFD.  /  LONG TERM: AEROSPACE & SPACE SYSTEMS.'},
    @{name='contact'; h=320; num='06'; tag='OPEN TO INTERNSHIPS & COLLABORATIONS'; title="LET'S BUILD"; title2='SOMETHING USEFUL.'; footer='THERMAL ENGINEERING  /  CFD  /  ENGINEERING SOFTWARE  /  APPLIED AI'}
)
$panelIndex = 0
foreach ($p in $panels) {
    $folder = Join-Path $framesRoot $p.name
    New-Item -ItemType Directory -Path $folder -Force | Out-Null
    # Sweeps stay in the bottom margin. All reading targets remain stationary.
    $frameCount = 240
    for ($frame=0; $frame -lt $frameCount; $frame++) {
        $t = $frame / [double]$frameCount
        $bmp = New-Object System.Drawing.Bitmap(1000, $p.h)
        $g = [System.Drawing.Graphics]::FromImage($bmp)
        $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
        $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
        $g.Clear($ink)
        # A twelve-second cosine sweep eases at both ends without a wrap jump.
        Rect $g $red 0 0 8 $p.h
        Rect $g ([System.Drawing.Color]::FromArgb(45, 229, 225, 216)) 32 ($p.h-28) 934 1
        $phase = $t + $panelIndex * 0.071
        $scan = 32 + 818 * (1 - [Math]::Cos($phase * 2 * [Math]::PI)) / 2
        Rect $g $red $scan ($p.h-30) 115 3
        Text $g $p.tag 36 23 13 $muted 'Arial' $true
        if ($p.num) {
            # Numerals and text stay fixed; only the marginal registration moves.
            $tone = 39
            Text $g $p.num 862 32 116 ([System.Drawing.Color]::FromArgb($tone, $tone+1, $tone+3)) 'Impact'
        }
        $titleSize = 66
        if ($p.title.Length -gt 20) { $titleSize = 57 }
        if ($p.title2) { $titleSize = 78 }
        Text $g $p.title 32 63 $titleSize $paper 'Impact'
        if ($p.title2) { Text $g $p.title2 32 143 $titleSize $paper 'Impact' }
        if ($p.footer) { Text $g $p.footer 36 ($p.h-61) 13 $muted 'Arial' $true }
        if ($p.rows) {
            $index = 0
            foreach ($row in $p.rows) {
                $y = 150 + $index * 43
                $color = $muted
                Text $g $row[0] 37 $y 13 $color 'Arial' $true
                Text $g $row[1] 184 ($y-3) 22 $paper
                $index++
            }
        }
        if ($p.metrics) {
            $index = 0
            foreach ($metric in $p.metrics) {
                $x = 36 + $index*310
                Text $g $metric[0] $x 143 44 $red 'Impact'
                Text $g $metric[1] $x 194 12 $muted 'Arial' $true
                $index++
            }
        }
        if ($p.columns) {
            $index = 0
            foreach ($col in $p.columns) {
                $x = 36 + $index*320
                Rect $g ([System.Drawing.Color]::FromArgb(48,49,51)) $x 149 280 2
                Text $g ($col[0]+' / '+$col[1]) $x 166 23 $red 'Impact'
                for ($line=2; $line -lt $col.Count; $line++) { Text $g $col[$line] $x (210+($line-2)*29) 17 $paper }
                $index++
            }
        }
        if ($p.principles) {
            $index=0
            foreach ($principle in $p.principles) {
                $y = 158 + $index*43
                $color=$paper
                Text $g ('0'+($index+1)) 42 $y 20 $red 'Impact'
                Text $g $principle 92 ($y+1) 21 $color
                $index++
            }
        }
        if ($p.stages) {
            $index = 0
            foreach ($stage in $p.stages) {
                $x = 36 + $index * 189
                Rect $g ([System.Drawing.Color]::FromArgb(44,45,47)) $x 157 166 135
                Rect $g $red $x 157 166 2
                Text $g $stage[0] ($x+12) 173 32 $red 'Impact'
                Text $g $stage[1] ($x+12) 213 21 $paper 'Impact'
                Text $g $stage[2] ($x+12) 251 14 $muted
                Text $g $stage[3] ($x+12) 270 14 $muted
                $index++
            }
        }
        $path = Join-Path $folder ('{0:D4}.png' -f $frame)
        $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
        if ($frame -eq 0) { $bmp.Save((Join-Path $assetsRoot ($p.name+'.png')), [System.Drawing.Imaging.ImageFormat]::Png) }
        $g.Dispose(); $bmp.Dispose()
    }
    # Explicit frame limit prevents stale frames from an earlier render entering a loop.
    & $FFmpeg -hide_banner -loglevel error -y -framerate 20 -i (Join-Path $folder '%04d.png') -filter_complex '[0:v]split[a][b];[a]palettegen=max_colors=128:stats_mode=diff[p];[b][p]paletteuse=dither=none' -frames:v $frameCount -loop 0 (Join-Path $assetsRoot ($p.name+'.gif'))
    if ($LASTEXITCODE -ne 0) { throw "Encoding failed for $($p.name)" }
    Write-Output "Rendered $($p.name)"
    $panelIndex++
}
