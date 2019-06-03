// components/slideshow/slideshow.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {

  },

  /**
   * 组件的初始数据
   */
  data: {
    currentTab: 0,
    imgUrls: [
      "slideImg/1.png", "slideImg/2.png", "slideImg/3.png", "slideImg/4.png", "slideImg/5.png",
    ]
  },

  /**
   * 组件的方法列表
   */
  methods: {
    clickSwiperTab: function(e) //点击swiperTab处理
    {
      var that = this;
      var currentTab = e.currentTarget.dataset.currenttabitem;
      console.log("page:collectBlessig-clickSwiperTab:currentTab", currentTab);
      that.setData({
        currentTab: currentTab,
      })
    },
    swiperTab: function(e) //滑动swiper处理
    {
      var that = this;
      that.setData({
        currentTab: e.detail.current
      });
    },
    preview:function(e){
      var img = e.currentTarget.dataset.img
      console.log(e)
      wx.previewImage({
        current: '0',
        urls: [img],
        success: function(res) {},
        fail: function(res) {},
        complete: function(res) {},
      })
    }
  }

})