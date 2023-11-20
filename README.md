# SphereMorph simulation

A simulation designed by Eli Kujawa to assist Christian Howard and Prof. Jeff Erickson in visualizing morphs of spherical projections of planar graphs.

## Using the simulation

Make sure you have numpy, scipy, and p5 installed prior to running the simulation.

Running any of the files in the "demos" folder will launch a window with a p5 simulation. The specifics of each particular animation are commented at the top of the files.

The read-and-plot.py file can read from any file in the shapes folder, and plot it in the simulation.

## Capabilities

The functions allowed in the simulation are all contained in the classes/graph.py file. Currently, they consist of:
- plotting a graph in 3D space
- plotting the graph's projection onto a sphere
- contracting 2 vertices towards each other
- applying any matrix transformation to the graph
- plotting the kernel of a graph

## "Breaking Lemmas"

This folder contains programs simulating some lemmas largely regarding convexification of spherically-embedded quadrilaterals. The goal is to test for counterexamples (and hopefully Not find any!).