package main

import "fmt"

type Graph map[string][]string

// Breadth first visit
// Time complexity
// O(V+E)
// V - visit node
// E - check edge
// Space complexit
// Visit stack O(V)
// Queue O(V)
// = O(V)
func visitNearestNeighhbor(start string, graph Graph) {
	visited := map[string]bool{}
	visitedOrder := []string{}
	tempQueue := []string{start}
	visitedOrder = append(visitedOrder, start)

	for len(tempQueue) > 0 {
		nodeStart := tempQueue[0]
		tempQueue = tempQueue[1:]
		visited[nodeStart] = true	
		
		fmt.Println("Visited: ", nodeStart)

		// E.g. A - C - B
		// Visit A, C, B - visit nearest neighbor immediately
		for _, neighbor := range graph[nodeStart] {
			if !visited[neighbor]{
				visited[neighbor]  = true
				visitedOrder = append(visitedOrder, neighbor)
				tempQueue = append(tempQueue, neighbor)
			}
		}
	}
	// VISITED NODES::  map[A:true B:true C:true D:true E:true]
	fmt.Println("VISITED NODES:: ", visited)

	// VISITED NODES IN ORDER OF VISITED::  [A C B E D]
	fmt.Println("VISITED NODES IN ORDER:: ", visitedOrder)

}

// Depth first visit
// Time complexity
// O(V+E)
// V - visit node
// E - check edge
// Space complexit
// Visit stack O(V)
// Queue O(V)
// = O(V)
func visitFarthesetNeighbor(start string, graph Graph , visited  map[string]bool ) {
	if visited[start] {
		return
	}

	// We visit the current node
	fmt.Println("Visited: ", start)
	visited[start] = true

	for _, neighbor := range graph[start] {
		visitFarthesetNeighbor(neighbor, graph, visited)
	}
}

func main() {
	graph := Graph{
		"A": {"B", "C"},
		"B": {"D"},
		"C": {"E"},
	}

	// Visited:  A
	// Visited:  B
	// Visited:  C
	// Visited:  D
	// Visited:  E
	// VISITED NODES::  map[A:true B:true C:true D:true E:true]
	// VISITED NODES IN ORDER::  [A B C D E]
	visitNearestNeighhbor("A", graph)

	fmt.Println("-------------------------------------")

	visited := map[string]bool{}
	visitFarthesetNeighbor("A", graph, visited)
	fmt.Println("Total visited: ", visited)
	// Visited:  A
	// Visited:  B
	// Visited:  D
	// Visited:  C
	// Visited:  E
	// Total visited:  map[A:true B:true C:true D:true E:true]
	
}
