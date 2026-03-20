<template>
  <div id="tube-graph"></div>
</template>

<script>
import ForceGraph3D from '3d-force-graph';
import * as THREE from 'three';

export default {
  name: 'TubeGraph',
  mounted() {
    fetch('domain/tube.json')
      .then(res => res.json())
      .then(data => {
        const myGraph = ForceGraph3D()(this.$el);
        // myGraph.graphData(data);
		myGraph
		.nodeRelSize(1) // Disable node size scaling
		.graphData(data)
		.zoomToFit(1000)
		.onNodeDragEnd(node=> {
			node.fx = node.x;
			node.fy = node.y;
			node.fz = node.z;
		})
		.nodeThreeObject(node => {
			// const nodeSize = typeof node.size === 'number' ? node.size : 5;  // Ensure node.size is a number, fallback to 5
			const nodeSize = node.size || 1;
			const nodeColor = node.color || "#FFFFFF";
			// Create a sphere geometry with the node's size
			const sphereGeometry = new THREE.SphereGeometry(nodeSize);
			const sphereMaterial = new THREE.MeshBasicMaterial({ color: nodeColor});
			const sphereMesh = new THREE.Mesh(sphereGeometry, sphereMaterial);
			
			return sphereMesh;
		})
		//.linkDirectionalParticles(1)
		//.linkDirectionalParticleWidth(3);
      })
      .catch(err => console.error(err));
  }
};
</script>

<style scoped>
#manifest-graph {
  width: 100%;
  height: 100vh;
}
</style>