<template>
  <v-app>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import MainPage from './components/MainPage';


export default {
  name: 'App',
  data: () => ({
    //
  }),
};
</script>
