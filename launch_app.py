import Covid.data.get_data as get_data
import Covid.data.process_JH_data as process_JH_data
import Covid.features.build_features as build_features


print("fetching data")
get_data.get_johns_hopkins()

print("processing_data")
process_JH_data.store_relational_JH_data()
process_JH_data.store_flat_table()


print("building features")
build_features.build_features_()

print("data_processed")
import Covid.visualization.visualize as visualize
visualize.app.run_server(debug=True, use_reloader=False)
