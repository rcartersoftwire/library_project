<div class="copy_info">
    <p>
    % if copies == 1:
        {{copies}} copy, {{copies_available}} currently available.
    % else:
        {{copies}} copies, {{copies_available}} currently available. 
    % end
    % if copies_available == 0:   
        Next due back: {{next_due}}
    % end
    </p>
</div>