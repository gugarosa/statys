from statys import measures, pairwise, significance

control = [0.82, 0.80, 0.84, 0.79]
model_a = [0.79, 0.77, 0.81, 0.75]
model_b = [0.75, 0.78, 0.76, 0.74]

print(measures.mean(control, model_a, model_b))

results = pairwise.signed_rank(control, model_a, model_b)
print(results)

significance.plot_p_value(
    results,
    labels=["Control", "Model A", "Model B"],
    output="p-values.pdf",
)
