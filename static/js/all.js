function updateCharts() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    document.getElementById('charts-container').innerHTML = '';

    fetchData(startDate, endDate);
}

async function fetchData(startDate, endDate) {
    try {
        // 날짜를 쿼리 매개변수로 포함하여 API 호출
        const response = await fetch(`/all?start_date=${startDate}&end_date=${endDate}`); // API 경로 수정
        const data = await response.json();

        // 데이터 확인
        console.log(data);

        // 데이터 형식 확인 및 처리
        if (data && data.data) {
            // 재료 카운트 차트 처리
            if (data.data.ingredient_count) {
                createBarChart('Ingredient Count', data.data.ingredient_count.ingredient, data.data.ingredient_count.count);
            }

            // 제품 카운트 차트 처리
            if (data.data.product_count) {
                createBarChart('Product Count', data.data.product_count.product, data.data.product_count.count);
            }

            // 회사 카운트 차트 처리
            if (data.data.company_count) {
                createBarChart('Company Count', data.data.company_count.company, data.data.company_count.count);
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

    // 색상을 랜덤하게 생성하는 함수
    const getRandomColor = () => {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    };

    // 데이터 항목 수만큼 색상 배열 생성
    const backgroundColors = data.map(() => getRandomColor());

    new Chart(ctx, {
        type: 'doughnut', // 도넛 차트로 설정
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: backgroundColors, // 생성한 색상 배열 사용
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                title: {
                    display: true,
                    text: label
                }
            }
        }
    });
}

// 페이지 로드 시 데이터 불러오기
fetchData();
