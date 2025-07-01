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
        // 首先嘗試從檔案清單載入
        await loadFromFileList();
    } catch (error) {
        console.error('無法從檔案清單載入資料:', error);
        // 如果失敗，嘗試從相對路徑載入
        try {
            await loadFromRelativePath();
        } catch (pathError) {
            console.error('無法從相對路徑載入資料:', pathError);
            // 最後嘗試從 GitHub API 載入
            try {
                await loadFromGitHub();
            } catch (apiError) {
                console.error('無法從 GitHub API 載入資料:', apiError);
                showEmptyState();
            }
        }
    }
}

// 從檔案清單載入資料
async function loadFromFileList() {
    console.log('📡 正在從檔案清單載入資料...');
    
    try {
        const response = await fetch('file-list.json');
        if (!response.ok) {
            throw new Error(`檔案清單請求失敗: ${response.status}`);
        }
        
        const fileList = await response.json();
        const batches = Object.keys(fileList).sort().reverse();
        
        console.log(`📁 從檔案清單找到 ${batches.length} 個批次:`, batches);
        
        if (batches.length === 0) {
            throw new Error('檔案清單中沒有批次');
        }
        
        allBatches = batches;
        
        // 載入每個批次的內容
        for (const batch of batches) {
            allScripts[batch] = [];
            const files = fileList[batch] || [];
            
            for (const fileInfo of files) {
                try {
                    // 載入文字檔案內容
                    const txtResponse = await fetch(`outputs/${batch}/${fileInfo.txt}`);
                    if (!txtResponse.ok) {
                        console.log(`無法載入 ${fileInfo.txt}`);
                        continue;
                    }
                    
                    const text = await txtResponse.text();
                    
                    allScripts[batch].push({
                        topic: fileInfo.name,
                        text: text,
                        txt: fileInfo.txt,
                        mp3: fileInfo.mp3,
                        txtUrl: `outputs/${batch}/${fileInfo.txt}`,
                        mp3Url: fileInfo.mp3 ? `outputs/${batch}/${fileInfo.mp3}` : null
                    });
                    
                    console.log(`✅ 載入檔案: ${fileInfo.name}`);
                } catch (error) {
                    console.error(`載入檔案 ${fileInfo.name} 時發生錯誤:`, error);
                }
            }
            
            console.log(`✅ 批次 ${batch} 載入完成，共 ${allScripts[batch].length} 個腳本`);
        }
        
        // 更新介面
        updateBatchSelector();
        displayScripts(batches[0]);
        
    } catch (error) {
        console.error('從檔案清單載入時發生錯誤:', error);
        throw error;
    }
}

// 從相對路徑載入資料（適用於 GitHub Pages）
async function loadFromRelativePath() {
    console.log('📡 正在從相對路徑載入資料...');
    
    // 嘗試載入已知的批次目錄
    const knownBatches = [
        '20250618_1531',
        '20250618_1545', 
        '20250618_1547',
        '20250618_1549'
    ];
    
    const validBatches = [];
    
    for (const batch of knownBatches) {
        try {
            // 嘗試載入這個批次的一個測試檔案
            const testResponse = await fetch(`outputs/${batch}/`, { method: 'HEAD' });
            if (testResponse.ok || testResponse.status === 403) { // 403 表示目錄存在但不能直接存取
                validBatches.push(batch);
            }
        } catch (error) {
            console.log(`批次 ${batch} 不存在或無法存取`);
        }
    }
    
    if (validBatches.length === 0) {
        throw new Error('沒有找到有效的批次');
    }
    
    allBatches = validBatches.sort().reverse();
    console.log(`📁 找到 ${allBatches.length} 個批次:`, allBatches);
    
    // 載入每個批次的檔案資訊
    await loadBatchDataFromPath(allBatches);
    
    // 更新介面
    updateBatchSelector();
    displayScripts(allBatches[0]);
}

// 從路徑載入批次資料
async function loadBatchDataFromPath(batches) {
    // 已知的檔案清單（您可以根據實際情況更新）
    const fileMapping = {
        '20250618_1531': [
            '仍持續敞開溝通大門_-_ETtoday新',
            '台南前副市長之子涉吸金上億失聯_顏大鈞深',
            '川普稱掌握伊朗最高領袖行蹤但暫不殺死似要',
            '川普要求無條件投降_伊朗最高領袖回敬「戰',
            '軍車3天奪2命！戰術輪車撞死上班途中女騎'
        ],
        '20250618_1545': [
            '下雨了！19縣市大雨特報恐一路下到晚上_',
            '伊朗最高領袖哈米尼稱「戰鬥開始了」_矢言',
            '台南前副市長之子涉吸金上億失聯_顏大鈞深',
            '無自覺跟反省_-_奇摩新聞',
            '黃國昌被質疑拿造假音檔質詢竟嗆她沒當過律'
        ],
        '20250618_1547': [
            '仍持續敞開溝通大門_-_ETtoday新',
            '台南前副市長之子涉吸金上億失聯_顏大鈞深',
            '川普稱掌握伊朗最高領袖行蹤但暫不殺死似要',
            '川普要求無條件投降_伊朗最高領袖回敬「戰',
            '早安世界》海鯤號首次海上測試駛出高雄港國'
        ],
        '20250618_1549': [
            '仍持續敞開溝通大門_-_ETtoday新',
            '台南前副市長之子涉吸金上億失聯_顏大鈞深',
            '川普稱掌握伊朗最高領袖行蹤但暫不殺死似要',
            '川普要求無條件投降_伊朗最高領袖回敬「戰',
            '早安世界》海鯤號首次海上測試駛出高雄港國'
        ]
    };
    
    for (const batch of batches) {
        const files = fileMapping[batch] || [];
        allScripts[batch] = [];
        
        for (const fileName of files) {
            try {
                // 載入文字檔案內容
                const txtResponse = await fetch(`outputs/${batch}/${fileName}.txt`);
                if (!txtResponse.ok) {
                    console.log(`無法載入 ${fileName}.txt`);
                    continue;
                }
                
                const text = await txtResponse.text();
                
                // 檢查是否有對應的 MP3 檔案
                const mp3Response = await fetch(`outputs/${batch}/${fileName}.mp3`, { method: 'HEAD' });
                const hasMP3 = mp3Response.ok;
                
                allScripts[batch].push({
                    topic: fileName,
                    text: text,
                    txt: `${fileName}.txt`,
                    mp3: hasMP3 ? `${fileName}.mp3` : null,
                    txtUrl: `outputs/${batch}/${fileName}.txt`,
                    mp3Url: hasMP3 ? `outputs/${batch}/${fileName}.mp3` : null
                });
                
                console.log(`✅ 載入檔案: ${fileName}`);
            } catch (error) {
                console.error(`載入檔案 ${fileName} 時發生錯誤:`, error);
            }
        }
        
        console.log(`✅ 批次 ${batch} 載入完成，共 ${allScripts[batch].length} 個腳本`);
    }
}

// 從 GitHub API 載入資料
async function loadFromGitHub() {
    // 自動檢測 GitHub 用戶名和倉庫名
    const currentUrl = window.location.href;
    let repoOwner, repoName;
    
    if (currentUrl.includes('github.io')) {
        // 從 GitHub Pages URL 解析
        const match = currentUrl.match(/https:\/\/([^.]+)\.github\.io\/([^\/]+)/);
        if (match) {
            repoOwner = match[1];
            repoName = match[2];
        }
    }
    
    // 如果無法自動檢測，使用預設值
    if (!repoOwner || !repoName) {
        repoOwner = 'YOUR_USERNAME'; // 這裡會被 GitHub Actions 替換
        repoName = 'regular-comix';
    }
    
    const apiUrl = `https://api.github.com/repos/${repoOwner}/${repoName}/contents/docs/outputs`;
    
    try {
        console.log('📡 正在從 GitHub API 載入資料...');
        console.log(`API URL: ${apiUrl}`);
        
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
        await loadBatchData(batches, repoOwner, repoName);
        
        // 更新介面
        updateBatchSelector();
        displayScripts(batches[0]);
        
    } catch (error) {
        console.error('載入 GitHub 資料時發生錯誤:', error);
        throw error;
    }
}

// 載入批次資料
async function loadBatchData(batches, repoOwner, repoName) {
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
    
    // 只添加有內容的批次選項
    const batchesWithContent = allBatches.filter(batch => {
        return allScripts[batch] && allScripts[batch].length > 0;
    });
    
    batchesWithContent.forEach(batch => {
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
    
    // 預設選擇最新的有內容批次
    if (batchesWithContent.length > 0) {
        batchSelect.value = batchesWithContent[0];
        const scriptCount = allScripts[batchesWithContent[0]] ? allScripts[batchesWithContent[0]].length : 0;
        batchInfo.textContent = `總共 ${scriptCount} 個漫畫腳本`;
    } else {
        batchInfo.textContent = '目前沒有可用的漫畫腳本';
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
