<template>
  <v-app>
    <v-app-bar app color="green darken-3" dense elevation="12">
    </v-app-bar>

    <v-main>
      <v-container>
        <v-row justify="center">
          <v-col v-for="(tile, index) in tiles" :key="index" cols="12" sm="4" md="3">

            <router-link :to="tile.link" style="text-decoration: none;">
              <v-card class="tile-card" elevation="0" @click="animateCard">
                <div class="img-container">
                  <v-img
                    class="align-end text-white"
                    max-width="100"
                    src="https://sig.strasbourg.eu/images/catalogue.png"
                  ></v-img>
                </div>
                <div class="card-bg" :style="{ backgroundImage: 'url(' + tile.imageUrl + ')' }"></div>
                <div class="title-container">
                  <v-card-title class="text-h4">{{ tile.title }}</v-card-title>
                </div>
                <v-card-text class="caption text-h6">{{ tile.description }}</v-card-text>
              </v-card>
            </router-link>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>
  
  <script>
  export default {
	data() {
	  return {
		tiles: [
		  { title: 'Tile 1', description: 'Description for Tile 1', link: '/catalog', imageUrl: 'https://via.placeholder.com/800x300' },
		  { title: 'Tile 2', description: 'Description for Tile 2', link: '/other-route', imageUrl: 'https://via.placeholder.com/800x300' },
		  { title: 'Tile 3', description: 'Description for Tile 3', link: '/some-route', imageUrl: 'https://via.placeholder.com/800x300' },
		  { title: 'Tile 4', description: 'Description for Tile 4', link: '/another-route', imageUrl: 'https://via.placeholder.com/800x300' },
		  { title: 'Tile 5', description: 'Description for Tile 5', link: '/another-route', imageUrl: 'https://via.placeholder.com/800x300' }
		]
	  };
	},
	methods: {
	  animateCard() {
		// Add your animation logic here
	  }
	}
  };
  </script>
  
  <style>
  .text-h6 {
	font-size: 18px;
  }
  
  .caption {
	font-size: 14px;
  }
  
  .tile-card {
	transition: transform 0.3s, box-shadow 0.3s;
	cursor: pointer;
	width: 100%;
	overflow: hidden;
	position: relative;
  }
  
  .card-bg {
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	background-size: cover;
	background-position: center;
	opacity: 0.8;
	z-index: -1;
	transition: opacity 0.3s;
  }
  
  .tile-card:hover {
	transform: translateY(-5px);
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .tile-card:hover .card-bg {
	opacity: 1;
  }
  .img-container {
  display: flex;
  justify-content: center;
}
  </style>
  