// 全域變數
let currentBatch = null;
let allBatches = [];
let allScripts = {};

// 當頁面載入完成時執行
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Regular Comix 靜態網站載入中...');
    loadData();
});

// 載入資料
async function loadData() {
    try {
        // 嘗試從 GitHub API 載入 outputs 目錄的資料
        await loadFromGitHub();
    } catch (error) {
        console.error('無法從 GitHub 載入資料:', error);
        showEmptyState();
    }
}

// 從 GitHub API 載入資料
async function loadFromGitHub() {
    const repoOwner = 'YOUR_USERNAME'; // 請替換為您的 GitHub 用戶名
    const repoName = 'regular-comix';
    const apiUrl = `https://api.github.com/repos/${repoOwner}/${repoName}/contents/docs/outputs`;
    
    try {
        console.log('📡 正在從 GitHub API 載入資料...');
        const response = await fetch(apiUrl);
        
        if (!response.ok) {
            throw new Error(`GitHub API 請求失敗: ${response.status}`);
        }
        
        const data = await response.json();
        const batches = data
            .filter(item => item.type === 'dir')
            .map(item => item.name)
            .sort()
            .reverse();
        
        console.log(`📁 找到 ${batches.length} 個批次:`, batches);
        
        if (batches.length === 0) {
            showEmptyState();
            return;
        }
        
        allBatches = batches;
        
        // 載入每個批次的檔案
        await loadBatchData(batches);
        
        // 更新介面
        updateBatchSelector();
        displayScripts(batches[0]);
        
    } catch (error) {
        console.error('載入 GitHub 資料時發生錯誤:', error);
        showEmptyState();
    }
}

// 載入批次資料
async function loadBatchData(batches) {
    const repoOwner = 'YOUR_USERNAME'; // 請替換為您的 GitHub 用戶名
    const repoName = 'regular-comix';
    
    for (const batch of batches) {
        try {
            console.log(`📝 載入批次 ${batch} 的內容...`);
            const batchUrl = `https://api.github.com/repos/${repoOwner}/${repoName}/contents/docs/outputs/${batch}`;
            const response = await fetch(batchUrl);
            
            if (!response.ok) continue;
            
            const files = await response.json();
            const txtFiles = files.filter(file => file.name.endsWith('.txt'));
            
            allScripts[batch] = [];
            
            for (const txtFile of txtFiles) {
                try {
                    // 載入文字檔案內容
                    const contentResponse = await fetch(txtFile.download_url);
                    if (!contentResponse.ok) continue;
                    
                    const text = await contentResponse.text();
                    const topic = txtFile.name.replace('.txt', '');
                    const mp3File = files.find(f => f.name === `${topic}.mp3`);
                    
                    allScripts[batch].push({
                        topic: topic,
                        text: text,
                        txt: txtFile.name,
                        mp3: mp3File ? mp3File.name : null,
                        txtUrl: txtFile.download_url,
                        mp3Url: mp3File ? mp3File.download_url : null
                    });
                } catch (error) {
                    console.error(`載入檔案 ${txtFile.name} 時發生錯誤:`, error);
                }
            }
            
            console.log(`✅ 批次 ${batch} 載入完成，共 ${allScripts[batch].length} 個腳本`);
        } catch (error) {
            console.error(`載入批次 ${batch} 時發生錯誤:`, error);
        }
    }
}

// 更新批次選擇器
function updateBatchSelector() {
    const batchSelect = document.getElementById('batch-select');
    const batchInfo = document.getElementById('batch-info');
    
    // 清空選項
    batchSelect.innerHTML = '<option value="">-- 選擇批次 --</option>';
    
    // 添加批次選項
    allBatches.forEach(batch => {
        const option = document.createElement('option');
        option.value = batch;
        option.textContent = formatBatchDate(batch);
        batchSelect.appendChild(option);
    });
    
    // 設定事件監聽器
    batchSelect.addEventListener('change', function() {
        const selectedBatch = this.value;
        if (selectedBatch) {
            displayScripts(selectedBatch);
        }
    });
    
    // 預設選擇最新批次
    if (allBatches.length > 0) {
        batchSelect.value = allBatches[0];
        const scriptCount = allScripts[allBatches[0]] ? allScripts[allBatches[0]].length : 0;
        batchInfo.textContent = `總共 ${scriptCount} 個漫畫腳本`;
    }
}

// 格式化批次日期
function formatBatchDate(batch) {
    if (batch.length >= 13) {
        const year = batch.substr(0, 4);
        const month = batch.substr(4, 2);
        const day = batch.substr(6, 2);
        const hour = batch.substr(9, 2);
        const minute = batch.substr(11, 2);
        return `${year}/${month}/${day} ${hour}:${minute}`;
    }
    return batch;
}

// 顯示腳本
function displayScripts(batch) {
    currentBatch = batch;
    const container = document.getElementById('scripts-container');
    const emptyState = document.getElementById('empty-state');
    const batchInfo = document.getElementById('batch-info');
    
    const scripts = allScripts[batch] || [];
    
    if (scripts.length === 0) {
        container.style.display = 'none';
        emptyState.style.display = 'block';
        batchInfo.textContent = '';
        return;
    }
    
    container.style.display = 'grid';
    emptyState.style.display = 'none';
    batchInfo.textContent = `總共 ${scripts.length} 個漫畫腳本`;
    
    // 生成腳本卡片
    container.innerHTML = scripts.map((script, index) => `
        <div class="comic-card">
            <div class="comic-header">
                <h2 class="comic-title">${escapeHtml(script.topic)}</h2>
                <span class="comic-index">#${index + 1}</span>
            </div>
            
            <div class="comic-content">
                <div class="script-text">
                    <h3>📝 漫畫腳本</h3>
                    <pre class="script-pre">${escapeHtml(script.text)}</pre>
                </div>
                
                <div class="audio-section">
                    <h3>🔊 語音播放</h3>
                    ${script.mp3Url ? `
                        <audio controls preload="metadata">
                            <source src="${script.mp3Url}" type="audio/mpeg">
                            您的瀏覽器不支援音訊播放。
                        </audio>
                    ` : '<p style="color: #666;">語音檔案不可用</p>'}
                    
                    <div class="download-links">
                        <a href="${script.txtUrl}" 
                           class="download-btn script-btn" 
                           download="${script.txt}">
                            📄 下載腳本
                        </a>
                        ${script.mp3Url ? `
                            <a href="${script.mp3Url}" 
                               class="download-btn audio-btn" 
                               download="${script.mp3}">
                                🎵 下載音檔
                            </a>
                        ` : ''}
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// 顯示空狀態
function showEmptyState() {
    const container = document.getElementById('scripts-container');
    const emptyState = document.getElementById('empty-state');
    const batchSelect = document.getElementById('batch-select');
    const batchInfo = document.getElementById('batch-info');
    
    container.style.display = 'none';
    emptyState.style.display = 'block';
    batchSelect.innerHTML = '<option value="">-- 暫無批次 --</option>';
    batchInfo.textContent = '';
}

// HTML 轉義函數
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

// 錯誤處理
window.addEventListener('error', function(event) {
    console.error('JavaScript 錯誤:', event.error);
});

// 未處理的 Promise 拒絕
window.addEventListener('unhandledrejection', function(event) {
    console.error('未處理的 Promise 拒絕:', event.reason);
    event.preventDefault();
});
