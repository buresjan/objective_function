#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Legacy VTK Reader'
file_data = LegacyVTKReader(registrationName='file_data', FileNames=['path_to_data'])

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
file_dataDisplay = Show(file_data, renderView1, 'UniformGridRepresentation')

# create a new 'Threshold'
threshold1 = Threshold(registrationName='Threshold1', Input=file_data)
threshold1.Scalars = ['POINTS', 'wall']
threshold1.ComponentMode = 'Selected'
threshold1.SelectedComponent = ''
threshold1.LowerThreshold = 0.0
threshold1.UpperThreshold = 0.5
threshold1.ThresholdMethod = 'Between'
threshold1.AllScalars = 1
threshold1.UseContinuousCellRange = 0
threshold1.Invert = 0
threshold1.MemoryStrategy = 'Mask Input'

# create a new 'Stream Tracer'
streamTracer1 = StreamTracer(registrationName='StreamTracer1', Input=threshold1,
    SeedType='Point Cloud')
streamTracer1.Vectors = ['POINTS', 'mean_velocity']
streamTracer1.InterpolatorType = 'Interpolator with Point Locator'
streamTracer1.SurfaceStreamlines = 0
streamTracer1.IntegrationDirection = 'BOTH'
streamTracer1.IntegratorType = 'Runge-Kutta 4-5'
streamTracer1.IntegrationStepUnit = 'Cell Length'
streamTracer1.SeedType.Center = [center_x, 0.0115345706, center_z]
streamTracer1.SeedType.Radius = 0.01
streamTracer1.SeedType.NumberOfPoints = 2500
streamTracer1.MaximumStreamlineLength = 50.0


# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=streamTracer1)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.UseDual = 0
slice1.Crinkleslice = 0
slice1.Triangulatetheslice = 1
slice1.SliceOffsetValues = [0.0]
slice1.PointMergeMethod = 'Uniform Binning'

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [0.08492784360714722, 0.011534570629009977, 0.03061601476292708]
slice1.SliceType.Normal = [1.0, 0.0, 0.0]
slice1.SliceType.Offset = 0.0

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice1.HyperTreeGridSlicer.Origin = [0.08492784360714722, 0.011534570629009977, 0.03061601476292708]
slice1.HyperTreeGridSlicer.Normal = [1.0, 0.0, 0.0]
slice1.HyperTreeGridSlicer.Offset = 0.0

# init the 'Uniform Binning' selected for 'PointMergeMethod'
slice1.PointMergeMethod.Divisions = [50, 50, 50]
slice1.PointMergeMethod.Numberofpointsperbucket = 8

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [0.005, 0.011534570629009977, 0.03061601476292708]

# set active source
SetActiveSource(streamTracer1)

# set active source
SetActiveSource(slice1)

# set active source
SetActiveSource(streamTracer1)

# create a new 'Slice'
slice2 = Slice(registrationName='Slice2', Input=streamTracer1)
slice2.SliceType = 'Plane'
slice2.HyperTreeGridSlicer = 'Plane'
slice2.UseDual = 0
slice2.Crinkleslice = 0
slice2.Triangulatetheslice = 1
slice2.SliceOffsetValues = [0.0]
slice2.PointMergeMethod = 'Uniform Binning'

# init the 'Plane' selected for 'SliceType'
slice2.SliceType.Origin = [0.08492235004814574, 0.011401064461097121, 0.03288479795810417]
slice2.SliceType.Normal = [1.0, 0.0, 0.0]
slice2.SliceType.Offset = 0.0

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice2.HyperTreeGridSlicer.Origin = [0.08492235004814574, 0.011401064461097121, 0.03288479795810417]
slice2.HyperTreeGridSlicer.Normal = [1.0, 0.0, 0.0]
slice2.HyperTreeGridSlicer.Offset = 0.0

# init the 'Uniform Binning' selected for 'PointMergeMethod'
slice2.PointMergeMethod.Divisions = [50, 50, 50]
slice2.PointMergeMethod.Numberofpointsperbucket = 8

# Properties modified on slice2.SliceType
slice2.SliceType.Origin = [0.165, 0.011401064461097121, 0.03288479795810417]

# set active source
SetActiveSource(slice1)

# set active source
SetActiveSource(streamTracer1)

# set active source
SetActiveSource(slice2)

# set active source
SetActiveSource(slice1)

# get layout
layout1 = GetLayout()

# split cell
layout1.SplitHorizontal(0, 0.5)

# set active view
SetActiveView(None)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.UseCache = 0
spreadSheetView1.ViewSize = [400, 400]
spreadSheetView1.CellFontSize = 9
spreadSheetView1.HeaderFontSize = 9
spreadSheetView1.SelectionOnly = 0
spreadSheetView1.GenerateCellConnectivity = 0
spreadSheetView1.ShowFieldData = 0
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.InvertOrder = 0
spreadSheetView1.BlockSize = 1024
spreadSheetView1.HiddenColumnLabels = ['Block Number']
spreadSheetView1.FieldAssociation = 'Cell Data'

# show data in view
slice1Display_1 = Show(slice1, spreadSheetView1, 'SpreadSheetRepresentation')

# trace defaults for the display properties.
slice1Display_1.Assembly = ''
slice1Display_1.BlockVisibilities = []

# assign view to a particular cell in the layout
AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=2)

# split cell
layout1.SplitVertical(2, 0.5)

# set active view
SetActiveView(None)

# Create a new 'SpreadSheet View'
spreadSheetView2 = CreateView('SpreadSheetView')
spreadSheetView2.UseCache = 0
spreadSheetView2.ViewSize = [400, 400]
spreadSheetView2.CellFontSize = 9
spreadSheetView2.HeaderFontSize = 9
spreadSheetView2.SelectionOnly = 0
spreadSheetView2.GenerateCellConnectivity = 0
spreadSheetView2.ShowFieldData = 0
spreadSheetView2.ColumnToSort = ''
spreadSheetView2.InvertOrder = 0
spreadSheetView2.BlockSize = 1024
spreadSheetView2.HiddenColumnLabels = ['Block Number']
spreadSheetView2.FieldAssociation = 'Cell Data'

# show data in view
slice1Display_2 = Show(slice1, spreadSheetView2, 'SpreadSheetRepresentation')

# trace defaults for the display properties.
slice1Display_2.Assembly = ''
slice1Display_2.BlockVisibilities = []

# assign view to a particular cell in the layout
AssignViewToLayout(view=spreadSheetView2, layout=layout1, hint=6)

# show data in view
slice2Display_1 = Show(slice2, spreadSheetView2, 'SpreadSheetRepresentation')

# trace defaults for the display properties.
slice2Display_1.Assembly = ''
slice2Display_1.BlockVisibilities = []

# set active view
SetActiveView(spreadSheetView1)

# export view
ExportView('LPA_path', view=spreadSheetView1, RealNumberNotation='Mixed', RealNumberPrecision=3)

# set active view
SetActiveView(spreadSheetView2)

# export view
ExportView('RPA_path', view=spreadSheetView2, RealNumberNotation='Mixed', RealNumberPrecision=3)
