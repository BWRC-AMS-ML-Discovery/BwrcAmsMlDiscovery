from example_server import auto_ckt_sim, AutoCktInput, AutoCktOutput  # FIXME: move

inp = AutoCktInput(3, 3, 3, 3, 3, 3, 1e-12)
out = auto_ckt_sim(inp)
print(out)
