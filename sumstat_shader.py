import pandas as pd
import holoviews as hv
import holoviews.operation.datashader as hd
import datashader as ds
import numpy as np
import panel as pn

from bokeh.models.tools import BoxZoomTool, PanTool

hv.extension("bokeh")

# TODO: add index SNP LD coloring

# other genome browser features
#   - gene track


def construct_ld_reference():
    pass


def construct_panel():
    # data preprocessing
    dat = pd.read_csv(
        "data/daner_0418b_gpc_lat_afr_sorted.gz",
        sep="\t",
        usecols=["CHR", "BP", "P"],
        nrows=100000,
    )

    dat["y"] = -np.log10(dat["P"])
    dat["x"] = dat.index

    hv.output(backend="bokeh")

    # toolbar
    zoom = BoxZoomTool(dimensions="width")
    pan = PanTool(dimensions="width")

    # plot
    points = hv.Points(dat.loc[:, ["x", "y"]])
    datashaded = hd.datashade(points, aggregator=ds.any())
    plt = hd.dynspread(datashaded, threshold=0.9, how="over", max_px=5, shape="square")
    plt.opts(responsive=True, tools=[zoom, pan], default_tools=["reset"])

    # UI
    panel = pn.Row(plt, sizing_mode="stretch_both")

    return panel


if __name__ == "__main__":
    panel = construct_panel()
    panel.servable()
