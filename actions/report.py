from output import notify
import config
import exporter
import subprocess
from output.notify import notification

def export_excel(days):
    templatePath = config.xlsx_template()
    outputPath = config.export_path()

    if not outputPath:
        raise ValueError('You must set an output file via --export_path="path/to/file" or via config.json')
    if not templatePath:
        raise ValueError('You must set a .xlsx template via --xlsx_template="path/to/file.xlsx" or via config.json')
    
    exporter.excel.export(days, templatePath, outputPath + ".xlsx")
    subprocess.call(["open", outputPath + ".xlsx"])
    notification('Export Done', 'Find your report at %s' % outputPath + ".xlsx")

def export_ods(days):
    templatePath = config.ods_template()
    outputPath = config.export_path()
    
    if not outputPath:
        raise ValueError('You must set an output file via --export_path="path/to/file" or via config.json')
    if not templatePath:
        raise ValueError('You must set a .ods template via --ods_template="path/to/file.ods" or via config.json')

    exporter.ods.export(days, templatePath, outputPath + ".ods")
    subprocess.call(["open", outputPath + ".ods"])
    notification('Export Done', 'Find your report at %s' % outputPath + ".ods")