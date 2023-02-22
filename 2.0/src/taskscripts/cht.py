from tasktools import data_tool

def run():
    dt = data_tool.DataTool("cht")
    params = dt.read_params()
    print(params)
    params["hi"] = 0
    dt.set_params(params)
    print(dt.read_params())
