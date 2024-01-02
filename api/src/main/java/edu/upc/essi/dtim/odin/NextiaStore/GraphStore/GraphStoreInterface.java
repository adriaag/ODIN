package edu.upc.essi.dtim.odin.NextiaStore.GraphStore;

import edu.upc.essi.dtim.NextiaCore.graph.Graph;

/**
 * Interface for a Graph Store that handles the storage and retrieval of graphs.
 */
public interface GraphStoreInterface {
    /**
     * Saves the given graph to the store.
     *
     * @param graph The graph to save.
     */
    void saveGraph(Graph graph);

    /**
     * Deletes the graph with the given name from the store.
     *
     * @param graph Graph to be deleted.
     */
    void deleteGraph(Graph graph);

    /**
     * Retrieves the graph with the given name from the store.
     *
     * @param name The URI of the graph to retrieve.
     * @return The retrieved graph.
     */
    Graph getGraph(String name);
}
