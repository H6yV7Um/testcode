(function() {
    class LocustLineChart {
        constructor(container, title, lines, unit) {
            this.container = $(container);
            this.title = title;
            this.lines = lines;
            
            this.element = $('<div class="locust-chart"></div>').css("width", "100%").appendTo(container);
            this.data = [];
            this.dates = [];
            
            this.seriesData = [];
            for (var i=0; i<lines.length; i++) {
                this.seriesData.push({
                    name: lines[i],
                    type: 'line',
                    showSymbol: true,
                    hoverAnimation: false,
                    data: [],
                });
                this.data.push([]);
            }
            
            this.chart = echarts.init(this.element[0], 'vintage');
            this.chart.setOption({
                title: {
                    text: this.title,
                    x: 10,
                    y: 10,
                },
                tooltip: {
                    trigger: 'axis',
                    formatter: function (params) {
                        if (!!params && params.length > 0 && !!params[0].value) {
                            var str = params[0].name;
                            for (var i=0; i<params.length; i++) {
                                var param = params[i];
                                str += '<br><span style="color:' + param.color + ';">' + param.seriesName + ': ' + param.data + '</span>';
                            }
                            return str;
                        } else {
                            return "No data";
                        }
                    },
                    axisPointer: {
                        animation: true
                    }
                },
                xAxis: {
                    type: 'category',
                    splitLine: {
                        show: false
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#5b6f66',
                        },
                    },
                    data: this.dates,
                },
                yAxis: {
                    type: 'value',
                    boundaryGap: [0, '100%'],
                    splitLine: {
                        show: false
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#5b6f66',
                        },
                    },
                },
                series: this.seriesData,
                grid: {x:60, y:70, x2:40, y2:40},
            })
        }
        
        addValue(values) {
            // this.dates.push(new Date().toLocaleTimeString());
            var dates = [];
            var data = [];
            for (var i=0; i< values.length; i++) {
                var datetime = new Date(values[i][0]);
                var locale_date_time = datetime.toLocaleString();
                // var locale_date_time = datetime.toLocaleTimeString();
                dates.push(locale_date_time);
                data.push(Math.round(values[i][1]));
            }
            this.chart.setOption({
                xAxis: {
                    data: dates,
                },
                series: [{
                        // type: 'line',
                        data: data
                    }
                ]
            });
        }
        
        resize() {
            this.chart.resize();
        }

        clear() {
            this.chart.clear();
        }

        showLoading(){
            this.chart.showLoading(
                {
                    text : '数据获取中',
                    color: '#c23531',
                    textColor: '#000',
                    maskColor: 'rgba(255, 255, 255, 0.8)',
                }
            );
        }

        hideLoading(){
            this.chart.hideLoading();
        }

        initChart() {
            this.chart.setOption({
                title: {
                    text: this.title,
                    x: 10,
                    y: 10,
                },
                tooltip: {
                    trigger: 'axis',
                    formatter: function (params) {
                        if (!!params && params.length > 0 && !!params[0].value) {
                            var str = params[0].name;
                            for (var i=0; i<params.length; i++) {
                                var param = params[i];
                                str += '<br><span style="color:' + param.color + ';">' + param.seriesName + ': ' + param.data + '</span>';
                            }
                            return str;
                        } else {
                            return "No data";
                        }
                    },
                    axisPointer: {
                        animation: true
                    }
                },
                xAxis: {
                    type: 'category',
                    splitLine: {
                        show: false
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#5b6f66',
                        },
                    },
                    data: this.dates,
                },
                yAxis: {
                    type: 'value',
                    boundaryGap: [0, '100%'],
                    splitLine: {
                        show: false
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#5b6f66',
                        },
                    },
                },
                series: this.seriesData,
                grid: {x:60, y:70, x2:40, y2:40},
            })
        }
    }
    window.LocustLineChart = LocustLineChart;
})();
