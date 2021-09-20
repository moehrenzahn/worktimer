import config
import exporter


def export(days):
    exporter.text.export(days, config.export_path() + ".txt")
