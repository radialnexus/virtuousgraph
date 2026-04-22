<template>
  <div class="side-panel">
    <div v-if="!selected" class="panel-welcome">
      <h2>Virtuous Graph</h2>
      <p>Click a node or edge to inspect its properties.</p>
      <div v-if="provenance" class="panel-provenance">
        <span class="provenance-label">Source:</span> {{ provenance }}
      </div>
    </div>
    <div v-else class="panel-content">
      <div class="panel-header">
        <span class="panel-type">{{ selected.type }}</span>
        <span class="panel-name">{{ selected.name || selected.id || '—' }}</span>
      </div>
      <div v-if="imageSrc" class="panel-image">
        <img :src="imageSrc" :alt="selected.name" @error="imageError = true" />
      </div>
      <table class="panel-properties">
        <tr v-for="(value, key) in displayProperties" :key="key">
          <td class="prop-key">{{ key }}</td>
          <td class="prop-value">{{ value }}</td>
        </tr>
      </table>
      <div class="panel-actions">
        <!-- Future: action buttons wired to graph functions -->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SidePanel',
  props: {
    selected: {
      type: Object,
      default: null
    },
    provenance: {
      type: String,
      default: null
    },
    imageBasePath: {
      type: String,
      default: 'images/trees'
    }
  },
  data() {
    return {
      imageError: false
    };
  },
  watch: {
    selected() {
      this.imageError = false;
    }
  },
  computed: {
    imageSrc() {
      if (!this.selected || !this.selected.name || this.imageError) return null;
      const name = this.selected.name
        .toLowerCase()
        .replace(/['']/g, '')
        .replace(/[^a-z0-9]+/g, '_')
        .replace(/^_|_$/g, '');
      return `${this.imageBasePath}/${name}.png`;
    },
    displayProperties() {
      if (!this.selected || !this.selected.properties) return {};
      const props = { ...this.selected.properties };
      delete props.image;
      return props;
    }
  }
};
</script>

<style scoped>
.side-panel {
  height: 100vh;
  background: #1a1a2e;
  color: #e0e0e0;
  padding: 20px;
  overflow-y: auto;
  border-left: 1px solid #2a2a4a;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 14px;
}

.panel-welcome h2 {
  color: #ffffff;
  margin: 0 0 12px 0;
  font-size: 18px;
}

.panel-welcome p {
  color: #888;
  margin: 0 0 20px 0;
}

.panel-provenance {
  margin-top: 20px;
  padding-top: 12px;
  border-top: 1px solid #2a2a4a;
  font-size: 12px;
  color: #666;
}

.provenance-label {
  color: #888;
}

.panel-header {
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #2a2a4a;
}

.panel-type {
  display: block;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #888;
  margin-bottom: 4px;
}

.panel-name {
  display: block;
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
  word-break: break-word;
}

.panel-image {
  margin-bottom: 16px;
  border-radius: 6px;
  overflow: hidden;
}

.panel-image img {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 6px;
}

.panel-properties {
  width: 100%;
  border-collapse: collapse;
}

.panel-properties tr {
  border-bottom: 1px solid #2a2a4a;
}

.panel-properties td {
  padding: 8px 0;
  vertical-align: top;
}

.prop-key {
  color: #888;
  width: 90px;
  font-size: 12px;
}

.prop-value {
  color: #e0e0e0;
  word-break: break-word;
}

.panel-actions {
  margin-top: 20px;
}
</style>
