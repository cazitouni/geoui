<template>
<v-toolbar color="green darken-3"  dense rounded elevation="12"  class="my-4 fixed-bar">
  <v-switch class="white--text ma-4" dark v-model="$vuetify.theme.dark" hint="Changer pour le mode nuit" inset label="Mode nuit" persistent-hint></v-switch>
  <v-text-field dark hide-details color="light-blue accent-3" prepend-icon="mdi-magnify" single-line></v-text-field>
</v-toolbar>
</template>

<style scoped>
.fixed-bar {
  width : 95%;
  position: sticky;
  position: -webkit-sticky;
  top: 0;
  z-index: 2;
}
</style>