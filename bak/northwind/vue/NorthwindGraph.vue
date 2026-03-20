<template>
  <div id="northwind-graph"></div>
</template>

<script>
import ForceGraph3D from '3d-force-graph';

export default {
  name: 'NorthwindGraph',
  mounted() {
    fetch('domain/northwind.json')
      .then(res => res.json())
      .then(data => {
        const myGraph = ForceGraph3D()(this.$el);
        myGraph.graphData(data);
      })
      .catch(err => console.error(err));
  }
};
</script>

<style scoped>
#trees-graph {
  width: 100%;
  height: 100vh;
}
</style>
