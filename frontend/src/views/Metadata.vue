<template>
    <div class="wrapper">
        <parallax class="section page-header header-filter" :style="headerStyle"></parallax>
        <div class="main main-raised">
            <div class="section">
                <div class="container">
                    <template v-for="(item, i) in items">
                                <h2 class="title text-center">{{i}}</h2>
                                <div class="md-layout">
            <div class="md-layout-item md-size-66 mx-auto">
                                <md-button v-bind:to="{ name : 'search', query : { where_metadata_label: i, where_metadata_value: j }}" v-for="(value, j) in item"><i class="fas fa-tag"></i> {{j}}: {{value}}</md-button>
    </div>
    </div>
</template>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { Badge } from "@/components";
import { Slider } from "@/components";

export default {
    components: {
        Badge,
        Slider,
    },
    bodyClass: "profile-page",
    data() {
        return {
            items: {},
            prefix: "http://localhost:5000"
            //prefix: "http://arctest06.dl.itc.u-tokyo.ac.jp"
        };
    },
    props: {
        header: {
            type: String,
            default: require("@/assets/img/bg7.jpg")
        }
    },
    computed: {
        headerStyle() {
            return {
                backgroundImage: `url(${this.header})`
            };
        }
    },
    methods: {
        search: function() {

            this.loading = true;

            this.items = {};

            const path = this.prefix+`/api/metadata`;

            axios
                .get(path)
                .then(response => {
                    this.loading = false;
                    this.items = response.data;
                    console.log(this.items)
                })
                .catch(error => {
                    console.log(error);
                });

        }
    },
    created() {
        this.search();
    }
};
</script>

<style lang="scss" scoped>
.page-header {
    height: 200px !important;
}
h1, h2 {
    font-family: "Roboto", "Helvetica", "Arial", sans-serif;
}
</style>