from jange import ops, stream, vis
ds = stream.from_csv(
    "https://raw.githubusercontent.com/jangedoo/jange/master/dataset/bbc.csv",
    columns="news",
    context_column="type",
)
# Extract clusters
result_collector = {}
clusters_ds = ds.apply(
    ops.text.clean.pos_filter("NOUN", keep_matching_tokens=True),
    ops.text.encode.tfidf(max_features=5000, name="tfidf"),
    ops.cluster.minibatch_kmeans(n_clusters=5),
    result_collector=result_collector,
)
# Get features extracted by tfidf and reduce the dimensions
features_ds = result_collector[clusters_ds.applied_ops.find_by_name("tfidf")]
reduced_features = features_ds.apply(ops.dim.pca(n_dim=2))

# Visualization
vis.cluster.visualize(reduced_features, clusters_ds)
