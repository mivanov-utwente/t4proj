phonon.options({
    navigator: {
        defaultPage: 'survey',
        enableBrowserBackButton: false,
    },
    i18n: null
});

phonon.navigator().on({page: 'survey'}, function(activity) {
    var currentTab = 1;
    var lastTabNumber = 0;
    var $tabsContainer;

    var _nextTab = function() {
        phonon.tab().setCurrentTab('survey', currentTab+1);
    };
    var _updateSubmitButtonSize = function() {
        var $btn = document.querySelector('.survey-submit-btn');
        var h = window.innerHeight;
        var bh = h / 2;
        var fs = Math.floor(bh/7);
        $btn.style.height = bh + 'px';
        $btn.style.width = bh + 'px';
        $btn.style.fontSize = fs + 'px';
    };

    activity.onCreate(function() {
        $tabsContainer = document.querySelector('[data-tab-contents="true"]')
        var tabs = $tabsContainer.querySelectorAll('.tab-content');
        lastTabNumber = tabs.length;
        var $nextTabBtns = document.querySelectorAll('.on-tap-next-tab');
        for (var i=0; i<$nextTabBtns.length; ++i){
            var tapTimer;
            $nextTabBtns[i].on('tap', function() {
                clearTimeout(tapTimer);
                tapTimer = setTimeout(_nextTab, 350);
            });
        }


    });
    activity.onTabChanged(function(tabNumber) {
        currentTab = tabNumber;
        var $title = document.querySelector('#survey-page-title');
        if (tabNumber == 1) {
            $title.innerHTML = $title.dataset.roomName;
        }
        else {
            $title.innerHTML = 'Step ' + (tabNumber-1) + ' / ' + (lastTabNumber-1);
        }

        var $tabContent = $tabsContainer.querySelector('.tab-content:nth-child('+ tabNumber +')');
        var $textareaEl = $tabContent.querySelector('textarea');
        if ($textareaEl) {
            var _focusTextArea = function (evt) {
                $textareaEl.focus();
                window.off(phonon.event.transitionEnd, _focusTextArea);
            };
            window.on(phonon.event.transitionEnd, _focusTextArea);
        }

        if (tabNumber == lastTabNumber) {
            _updateSubmitButtonSize();

        }
    });
    window.on('resize', function(evt) {
        if (currentTab == lastTabNumber) {
            _updateSubmitButtonSize();
        }
    }, false);
});

phonon.navigator().start();