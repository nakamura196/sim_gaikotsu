<template>
    <footer class="footer"
            :class="{[`footer-${type}`]: type}"
            :data-background-color="backgroundColor">
        <div class="container">
            <nav>
                <ul>
                    <li>
                        <a href="https://iiif.dl.itc.u-tokyo.ac.jp/repo/s/gaikotsu/page/home">
                            宮武外骨蒐集資料
                        </a>
                    </li>
                </ul>
            </nav>
            <div class="copyright">
                東京大学学術資産等アーカイブズ委員会事務局<br/>
                （東京大学附属図書館総務課／<br/>
                学術資産アーカイブ化推進室）<br/>
                E-mail：digital-archive [at] lib.u-tokyo.ac.jp
                <hr/>
                Design from <a href="https://www.creative-tim.com/">Creative Tim</a>.
            </div>
        </div>
    </footer>
</template>
<script>
export default {
  props: {
    backgroundColor: String,
    type: String
  },
  data() {
    return {
      year: new Date().getFullYear()
    };
  }
};
</script>
<style>
</style>
