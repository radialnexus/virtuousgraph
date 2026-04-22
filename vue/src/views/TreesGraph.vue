<template>
  <div class="app-layout">
    <MenuBar :currentDomain="currentDomain" @open-domain="loadDomain" />
    <div class="graph-layout">
      <div class="graph-container" ref="graphContainer"></div>
      <div
        class="divider"
        @mousedown="startResize"
      ></div>
      <SidePanel
        :selected="selected"
        :provenance="provenance"
        :style="{ width: panelWidth + 'px', minWidth: panelWidth + 'px' }"
      />
    </div>
  </div>
</template>

<script>
import ForceGraph3D from '3d-force-graph';
import SidePanel from '../components/SidePanel.vue';
import MenuBar from '../components/MenuBar.vue';

export default {
  name: 'TreesGraph',
  components: { SidePanel, MenuBar },
  data() {
    return {
      selected: null,
      provenance: null,
      panelWidth: 320,
      currentDomain: 'trees'
    };
  },
  methods: {
    loadDomain(domain) {
      this.currentDomain = domain.id;
      this.selected = null;
      this.provenance = domain.file;
      this.loadGraph(domain.file);
    },
    loadGraph(jsonPath) {
      fetch(jsonPath)
        .then(res => res.json())
        .then(data => {
          const container = this.$refs.graphContainer;

          // Clear previous graph
          if (this._graph) {
            this._graph._destructor && this._graph._destructor();
            container.innerHTML = '';
          }

          const graph = ForceGraph3D()(container);
          this._graph = graph;

          graph
            .width(container.offsetWidth)
            .height(container.offsetHeight)
            .graphData(data)
            .nodeLabel('')
            .linkLabel('')
            .onNodeClick(node => {
              const properties = {};
              Object.keys(node).forEach(key => {
                if (!['__threeObj', 'index', 'vx', 'vy', 'vz', 'x', 'y', 'z'].includes(key)) {
                  properties[key] = node[key];
                }
              });
              this.selected = {
                type: 'Node',
                name: node.name,
                id: node.id,
                properties
              };
            })
            .onLinkClick(link => {
              const properties = {};
              Object.keys(link).forEach(key => {
                if (!['__lineObj', '__arrowObj', '__curve', 'index', 'source', 'target'].includes(key)) {
                  properties[key] = link[key];
                }
              });
              properties['source'] = link.source.name || link.source.id || link.source;
              properties['target'] = link.target.name || link.target.id || link.target;
              this.selected = {
                type: 'Edge',
                name: link.name || link.relationship || '—',
                properties
              };
            });
        })
        .catch(err => console.error(err));
    },
    startResize(e) {
      e.preventDefault();
      const startX = e.clientX;
      const startWidth = this.panelWidth;

      const onMove = (moveEvent) => {
        const delta = startX - moveEvent.clientX;
        const newWidth = Math.min(
          Math.max(startWidth + delta, 200),
          window.innerWidth - 400
        );
        this.panelWidth = newWidth;
        this.resizeGraph();
      };

      const onUp = () => {
        document.removeEventListener('mousemove', onMove);
        document.removeEventListener('mouseup', onUp);
        document.body.style.cursor = '';
        document.body.style.userSelect = '';
      };

      document.body.style.cursor = 'col-resize';
      document.body.style.userSelect = 'none';
      document.addEventListener('mousemove', onMove);
      document.addEventListener('mouseup', onUp);
    },
    resizeGraph() {
      if (this._graph) {
        const container = this.$refs.graphContainer;
        this._graph.width(container.offsetWidth).height(container.offsetHeight);
      }
    }
  },
  mounted() {
    this.provenance = 'domain/trees.json';
    this.loadGraph('domain/trees.json');

    this._onResize = () => {
      this.resizeGraph();
    };
    window.addEventListener('resize', this._onResize);
  },
  beforeUnmount() {
    if (this._onResize) {
      window.removeEventListener('resize', this._onResize);
    }
  }
};
</script>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.graph-layout {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.graph-container {
  flex: 1;
  min-width: 400px;
}

.divider {
  width: 5px;
  cursor: col-resize;
  background: #2a2a4a;
  transition: background 0.15s;
}

.divider:hover {
  background: #4a4a8a;
}
</style>
