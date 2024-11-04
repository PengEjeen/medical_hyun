function updateCharts() {
    const company = document.getElementById('company').value;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    document.getElementById('charts-container').innerHTML = '';

    fetchData(company, startDate, endDate);
}

async function fetchData(company = '경동제약(주)', startDate = '2023-01-01', endDate = '2023-12-31') {
    try {
        // 쿼리 파라미터 추가
        const queryParams = new URLSearchParams({
            company: company,
            start_date: startDate,
            end_date: endDate
        });

        // 수정된 API 요청 경로
        const response = await fetch(`/ingredient?${queryParams.toString()}`);
        const data = await response.json();

        // 데이터 확인
        console.log(data);

        // 기존 데이터 처리 로직
        if (data && data.data) {
            if (data.data.count_result) {
                data.data.count_result.forEach(item => {
                    const company = item.company;
                    const labels = item.data.ingredient;
                    const chartData = item.data.count;
                    
                    if (labels.length > 0 && chartData.length > 0) {
                        createBarChart(company, labels, chartData);
                    }
                });
            }

            if (data.data.time_result) {
                data.data.time_result.forEach(item => {
                    const company = item.company;
                    const ingredient = item.ingredient;
                    const labels = item.data.time;
                    const chartData = item.data.count;

                    if (labels.length > 0 && chartData.length > 0) {
                        createLineChart(company + ' - ' + ingredient, labels, chartData);
                    }
                });
            }
        } else {
            console.error("Invalid data format");
        }
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

// 바 차트 생성 함수
function createBarChart(label, labels, data) {
    const ctx = document.createElement('canvas');
    document.getElementById('charts-container').appendChild(ctx);

    new Chart(ctx, {
        type: 'bar', // 바 차트로 설정
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                },
                x: {
                    title: {
                        display: true,
                        text: 'Ingredients'
                    }
                }
            }
        }
    });
}

// 선형 차트 생성 함수
function createLineChart(label, labels, data) {
    const ctx = document.createElement('canvas');
    document.getElementById('charts-container').appendChild(ctx);

    new Chart(ctx, {
        type: 'line', // 선형 차트로 설정
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: true // 영역을 채우기 원할 경우 true
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                },
                x: {
                    title: {
                        display: true,
                        text: 'Time'
                    }
                }
            }
        }
    });
}

// 페이지 로드 시 데이터 불러오기
fetchData();
