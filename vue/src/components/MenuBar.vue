<template>
  <div class="menu-bar">
    <div class="menu-item" @click="toggleMenu('file')" @mouseleave="closeMenu">
      <span>File</span>
      <div v-if="openMenu === 'file'" class="dropdown">
        <div class="dropdown-label">Open Domain</div>
        <div
          v-for="domain in domains"
          :key="domain.id"
          class="dropdown-item"
          :class="{ active: domain.id === currentDomain }"
          @click.stop="selectDomain(domain)"
        >
          {{ domain.label }}
        </div>
      </div>
    </div>
    <div class="menu-item disabled">Edit</div>
    <div class="menu-item disabled">View</div>
    <div class="menu-spacer"></div>
    <div class="menu-domain">{{ currentLabel }}</div>
  </div>
</template>

<script>
export default {
  name: 'MenuBar',
  props: {
    currentDomain: {
      type: String,
      default: 'trees'
    }
  },
  data() {
    return {
      openMenu: null,
      domains: [
        { id: 'trees', label: 'Exceptional Trees (Hawaii)', file: 'domain/trees.json' },
        { id: 'colors', label: 'RGB Colors', file: 'domain/colors.json' },
        { id: 'tube', label: 'London Underground', file: 'domain/tube.json' },
        { id: 'northwind', label: 'Northwind', file: 'domain/northwind.json' }
      ]
    };
  },
  computed: {
    currentLabel() {
      const d = this.domains.find(d => d.id === this.currentDomain);
      return d ? d.label : '';
    }
  },
  methods: {
    toggleMenu(menu) {
      this.openMenu = this.openMenu === menu ? null : menu;
    },
    closeMenu() {
      setTimeout(() => { this.openMenu = null; }, 150);
    },
    selectDomain(domain) {
      this.openMenu = null;
      this.$emit('open-domain', domain);
    }
  }
};
</script>

<style scoped>
.menu-bar {
  display: flex;
  align-items: center;
  height: 32px;
  background: #1a1a2e;
  border-bottom: 1px solid #2a2a4a;
  padding: 0 12px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 13px;
  color: #e0e0e0;
  user-select: none;
}

.menu-item {
  position: relative;
  padding: 4px 12px;
  cursor: pointer;
  border-radius: 4px;
}

.menu-item:hover {
  background: #2a2a4a;
}

.menu-item.disabled {
  color: #555;
  cursor: default;
}

.menu-item.disabled:hover {
  background: transparent;
}

.menu-spacer {
  flex: 1;
}

.menu-domain {
  font-size: 12px;
  color: #888;
}

.dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 4px;
  background: #1e1e38;
  border: 1px solid #2a2a4a;
  border-radius: 6px;
  padding: 4px 0;
  min-width: 220px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  z-index: 100;
}

.dropdown-label {
  padding: 6px 14px;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #666;
}

.dropdown-item {
  padding: 8px 14px;
  cursor: pointer;
}

.dropdown-item:hover {
  background: #2a2a4a;
}

.dropdown-item.active {
  color: #7a9ff0;
}
</style>
