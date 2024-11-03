async function fetchData() {
    try {
        const response = await fetch('/product?company=경동제약(주)'); // API 경로 수정
        const data = await response.json();

        // 데이터 확인
        console.log(data);

        // 데이터 형식 확인 및 처리
        if (data && data.data) {
            // count_result 처리
            if (data.data.count_result) {
                data.data.count_result.forEach(item => {
                    const company = item.company;
                    const labels = item.data.product; // x축 레이블
                    const chartData = item.data.count; // y축 데이터
                    
                    // 데이터가 비어있지 않을 경우에만 차트를 생성
                    if (labels.length > 0 && chartData.length > 0) {
                        createBarChart(company, labels, chartData);
                    }
                });
            }

            // time_result 처리
            if (data.data.time_result) {
                data.data.time_result.forEach(item => {
                    const company = item.company;
                    const product = item.product;
                    const labels = item.data.time; // x축 레이블
                    const chartData = item.data.count; // y축 데이터

                    // 데이터가 비어있지 않을 경우에만 차트를 생성
                    if (labels.length > 0 && chartData.length > 0) {
                        createLineChart(company + ' - ' + product, labels, chartData);
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
                        text: 'products'
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
