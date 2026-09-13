<style>
    .non-threat {
        color: grey
    }

    .low {
    color: green
    }

    .medium {
    color: orange
    }

    .high {
    color: red
    }

    .critical {
    color: rgb(163, 0, 0)
    }
</style>

## Refactor Journal
**Refactoring logs only contain threats, vulnerabilities and risks that were present due to AI's mistakes.**
### Key
#### Reasons for refactor
**Threat**: A block of code, package used or module poses a serious security risk.<br>**Vulnerability**: A block of code, package used or module poses a medium or lower security risk.<br>**Risk**: Any other non-security risk that involves bad practise or impacts software quality negatively.<br>
#### Severity
<span class="non-threat">**Non-threat**</span><br><span class="low">**Low**</span><br><span class="medium">**Medium**</span><br><span class="high">**High**</span><br><span class="critical">**Critical**</span>

| Issue | Date & Time | Description | Refactor | 
| :---: | :--- | :--- | :--- |
| **1** | 05/09/26<br>18:33 | <span class="critical">**Threat (Critical)**</span>: Gemini used two outdated packages which are abandoned (`passlib.context`,`python-jose`) in the module `security.py`, this can result in severe security vulnerabilities, as security keys can easily obtained or cracked, as `python-jose` stores the secret key internally using a raw string. Additionally, `passlib.context` is an abandoned package that has not received a stable release, leading to runtime errors and outdated security measures. | Refactored code logic to use `joserfc`, a newer and more modern package that handles secret keys more securely by never storing them as a raw-string, it must be imported as a mathematically verified JWK object (JSON Web Key) before any cryptographic actions are performed. Used `pwdlib` instead of `passlib.context` as it recieves regular updates and poses minimal security risks.|