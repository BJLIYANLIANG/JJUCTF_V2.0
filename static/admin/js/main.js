/**
 * Created by admin on 2016/12/13.
 */

/** ============== 第三方JS的预定义及配置 ============== **/
(function($) {
    // 配置模板
    /**
    * 名称：
    * 功能：
    * 依赖：xxx.min.css、xxx.min.js
    */
    (function() {

    })();

    /**
    * 名称：jquery通知提示插件toastr
    * 功能：jquery通知提示插件toastr的初始化配置
    * 依赖：toastr.min.css、toastr.min.js
    */
    (function() {
        try {
            toastr.options = {
                closeButton: true,
                debug: false,
                progressBar: false,
                positionClass: "toast-top-right",
                onclick: null,
                showDuration: "300",
                hideDuration: "1000",
                timeOut: "5000",
                extendedTimeOut: "1000",
                showEasing: "swing",
                hideEasing: "linear",
                showMethod: "fadeIn",
                hideMethod: "fadeOut"
            };
        } catch(err) {
            console.warn(err);
        }
    })();

})(jQuery);
/** ============== 第三方JS的预定义及配置 ============== **/

/** ============== 网站基础JS组件定义及应用 ============== **/
(function($) {

    /**
     * 默认选择器：.sidebar-menu
     * 功能：初始化左侧导航栏
     * @param opts
     */
    $.fn.initSidebarMenu = function(opts) {
        var defaults = {
            activedClass: 'actived',
            menuSelector: '.menu-list',
            menuItemSelector: '.menu-item',
            subMenuSeletor: '.sub-menu-list',
            subMenuItemSeletor: '.sub-menu-item'
        };
        var options = $.extend(defaults, opts);

        var $self = $(this);
        var $menuItem = $self.find(options.menuItemSelector);

        $self.find(options.menuSelector + '>' + options.menuItemSelector + '>a').on('click', function() {

            var $parent = $(this).parents(options.menuItemSelector);
            if($parent.hasClass(options.activedClass)) {
                $menuItem.removeClass(options.activedClass);
            } else {
                $menuItem.removeClass(options.activedClass);
                $parent.addClass(options.activedClass);
            }
        });
    };

    /**
     * 默认选择器：navbar-sidebar-toggle
     * 功能：展开或收缩左侧导航栏
     * @param opts
     */
    $.fn.initNavBarToggle = function(opts) {
        var defaults = {
            sidebarMenuSelector: '.sidebar-menu',
            sidebarCollapsedClass: 'collapsed',
            mainContainerSelector: '.main-container',
            mainContainerStretchedClass: 'stretched'
        };
        var options = $.extend(defaults, opts);
        var $sidebar = $(options.sidebarMenuSelector);
        var $container = $(options.mainContainerSelector);
        var collapsed = options.sidebarCollapsedClass;
        var streched = options.mainContainerStretchedClass;

        var fnCollapsed = function() {
            $sidebar.addClass(collapsed);
            $container.addClass(streched);
        };

        var fnShown = function() {
            $sidebar.removeClass(collapsed);
            $container.removeClass(streched);
        };

        $(this).on('click', function() {
            if($sidebar.hasClass(collapsed)) {
                fnShown();
            } else {
                fnCollapsed();
            }
        });

        var $win = $(window);
        var fnListenWinWidth = function() {
            if($win.width() <= 650) {
                if(!$sidebar.hasClass(collapsed)) {
                    fnCollapsed();
                }
            } else {
                if($sidebar.hasClass(collapsed)) {
                    fnShown();
                }
            }
        };
        $win.on('resize', fnListenWinWidth);
        $(document).ready(fnListenWinWidth);
    };

    /**
     * 默认选择器：.scroll-to-top
     * 功能：回到顶部的功能
     */
    $.fn.initScrollToTop = function(opts) {
        var defaults = {
            scrollObjSelector: '.wrapper', // 监听滚动的对象的选择器
            activedClass: 'shown'
        };
        var options = $.extend(defaults, opts);

        var $container = $(options.scrollObjSelector);
        var $self = $(this);
        var shown = options.activedClass;
        $container.on('scroll', function() {
            if($(this).scrollTop() > 300) {
                $self.addClass(shown);
            } else {
                $self.removeClass(shown);
            }
        });

        $self.on('click', function() {
            $container.animate({'scrollTop': 0});
        });
    };

    /**
     * 条件：需要设置一个modal在页面中作为confirm提示窗口，同时设置该modal的id为#modal-confirm（可修改），设置确定按钮的class为.modal-btn-sure（可修改）；
     *      设置调出该modal的链接a或span或按钮的一个 data-url 属性，作为modal确定按钮访问的链接
     * 功能：以modal形式弹出confirm窗口，并响应确定按钮的事件，可用在像删除、撤销订单的功能上
     * @param opts
     */
    $.fn.showConfirm = function(opts) {
        var defaults = {
            modalSelector: '#modal-confirm', // modal提示框的选择器
            btnSureSelector: '.modal-btn-sure', // modal中的确定按钮的选择器

            pre: function() { // 在$(this)被点击后的操作

            },
            success: function(url) { // 成功回调
                alert('提示：操作成功！');
            },
            error: function(err) { // 失败回调
                alert('提示：操作失败！');
            }
        };
        var option = $.extend(defaults, opts);

        var $modal = $(option.modalSelector);
        var $input = $(option.modalSelector + ' input[type=hidden]');

        $(this).on('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            option.pre.call(this);

            var $this = $(this);
            $input.val($this.data('url'));
            $modal.modal('show');
        });
        $(option.btnSureSelector).on('click', function() {
            var url = $input.val();
            if(url) {

                //window.location.href = url;
                // 进行确定操作
                option.success(url);

            } else {
                option.error('error: 获取url失败！');
            }
            $modal.modal('hide');
        });
    };


    /**
     * 默认选择器：.box .box-toggle
     * 功能：展开和收起盒子
     * @param opts
     */
    $.fn.initToggleBox = function(opts) {
        var defaults = {
            boxSelector: '.box',
            collapsedClass: 'collapsed',
            openIcon: '<i class="fa fa-chevron-up"></i>',
            closeIcon: '<i class="fa fa-chevron-down"></i>'
        };
        var options = $.extend(defaults, opts);

        var collapsed = options.collapsedClass;
        var $self = $(this);
        $self.on('click', function() {
            var $this = $(this);
            var $box = $this.parents(options.boxSelector);
            if($box.hasClass(collapsed)) { // 盒子收起状态
                $this.html(options.openIcon);
                $box.removeClass(collapsed);
            } else { // 盒子展开状态
                $this.html(options.closeIcon);
                $box.addClass(collapsed);
            }
        });
    };


    /**
     * 默认选择器：.input-daterange
     * 功能：使用DateRangePicker插件实现时间范围的选择
     * @param callback
     */
    $.fn.setDateRangePicker = function(callback) {

        var $this = $(this);
        try {
            $this.daterangepicker({
                "locale": {
                    "format": "YYYY/MM/DD",
                    "separator": " - ",
                    "applyLabel": "确定",
                    "cancelLabel": "取消",
                    "fromLabel": "From",
                    "toLabel": "To",
                    "customRangeLabel": "Custom",
                    "weekLabel": "W",
                    "daysOfWeek": [
                        "日",
                        "一",
                        "二",
                        "三",
                        "四",
                        "五",
                        "六"
                    ],
                    "monthNames": [
                        "一月",
                        "二月",
                        "三月",
                        "四月",
                        "五月",
                        "六月",
                        "七月",
                        "八月",
                        "九月",
                        "十月",
                        "十一月",
                        "十二月"
                    ],
                    "firstDay": 1
                },
                "applyClass": "btn-success btn-flat",
                "cancelClass": "btn-default no-border-radius"
            }, function(start, end, label) {
                // console.log("New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')");
                // console.log(start, end, label);
            });
        } catch(err) {
            console.warn(err);
        }

        $this.val('');
        $this.on('blur', function() {
            $(this).val('');
        });
        $this.on('change', function() {
            var date = $(this).val();
            var arr = date.split(' - ');
            //var startTime = (Date.parse(new Date(arr[0] + ' 00:00:00'))) / 1000;
            //var endTime = (Date.parse(new Date(arr[1] + ' 23:59:59'))) / 1000;

            var startTime = new Date(Date.parse((arr[0] + ' 00:00:00').replace(/-/g, '/'))).getTime() / 1000;
            var endTime = new Date(Date.parse((arr[1] + ' 23:59:59').replace(/-/g, '/'))).getTime() / 1000;

            if(callback) {
                callback(startTime, endTime);
            }
        });
    };

    /**
     * 功能：初始化复选框全选功能
     */
    $.fn.initCheckAll = function(opts) {
        var defaults = {
            childSelector: '.child-cb',
            trCanSelected: true // 是否行被点击也可以选中
        };
        var options = $.extend(defaults, opts);

        var $self = $(this);
        var $childs = $(options.childSelector);
        var childsLen = $childs.length; // 子复选框的长度

        $self.on('click', function() {
            $childs.prop('checked', $(this).prop('checked'));
        });

        $childs.on('click', function(e) {
            e.stopPropagation();
            var $checkedChilds = $(options.childSelector + ':checked');
            if(childsLen == $checkedChilds.length) {
                $self.prop('checked', true);
            } else {
                $self.prop('checked', false);
            }
        });

        // 是否行被点击也可以选中
        if(options.trCanSelected) {
            var $tr = $childs.parents('tr');

            $tr.on('click', function() {
                var $cb = $(this).find(options.childSelector);
                $cb.prop('checked', !$cb.prop('checked'));

                var $checkedChilds = $(options.childSelector + ':checked');
                if(childsLen == $checkedChilds.length) {
                    $self.prop('checked', true);
                } else {
                    $self.prop('checked', false);
                }
            });

            // a 元素阻止事件冒泡
            $tr.find('a').on('click', function(e) {
                e.stopPropagation();
            });
        }
    };

    // 初始化侧边导航栏
    $('.sidebar-menu').initSidebarMenu();
    // 初始化侧边导航栏开关
    $('.navbar-sidebar-toggle').initNavBarToggle();
    // 初始化工具提示
    $("[data-toggle='tooltip']").tooltip();
    // 初始化回到顶部按钮
    $('.scroll-to-top').initScrollToTop();
    // 初始化盒子开关按钮
    $('.box .box-toggle').initToggleBox();
})(jQuery);
/** ============== 网站基础JS组件定义及应用 ============== **/


/** ============== 针对网站需求的公共函数定义 ============== **/
/**
* 功能：xxx
*/
function templateFn() {

}

/** ============== 针对网站需求的公共函数定义 ============== **/


/** ============== 针对网站需求的逻辑JS组件定义 ============== **/
(function($) {

    /**
     * 默认选择器：
     * 样式：（默认选择器的样式）
     * 条件：（无）
     * 功能：
     * @param opts
     */
    $.fn.template = function(opts) {
        var defaults = {

        };
        var options = $.extend(defaults, opts);

        // 具体逻辑定义
        var $self = $(this);

    };

})(jQuery);
/** ============== 针对网站需求的逻辑JS组件定义 ============== **/


/** ============== 针对网站需求的JS组件应用定义 ============== **/
(function($) {

    // 使用示例
    /**
    * 功能：
    * 应用：xxx.html、xxx.html
    */
    $('.temp').template();


})(jQuery);
/** ============== 针对网站需求的JS组件应用定义 ============== **/