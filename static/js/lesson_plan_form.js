document.addEventListener('DOMContentLoaded', function() {
    const durationSelect = document.querySelector('.duration-select');
    const customDurationInput = document.querySelector('.custom-duration');

    function toggleCustomDuration() {
        if (durationSelect.value === 'custom') {
            customDurationInput.style.display = 'block';
            customDurationInput.required = true;
        } else {
            customDurationInput.style.display = 'none';
            customDurationInput.required = false;
        }
    }

    // 初始化时检查
    toggleCustomDuration();

    // 监听选择变化
    durationSelect.addEventListener('change', toggleCustomDuration);
}); 